import json
import os
import sys
import time
import atexit
import requests
import logging
import socket
import threading
import selectors
import signal
import queue
import struct  
from types import TracebackType
from typing import Any, Dict, Optional, Type, List, Tuple, Union, cast
import secrets
import string
import orjson 

# --- JSON Serialization ---
def _json_dumps(obj: Any) -> bytes:
    # orjson returns bytes
    return orjson.dumps(obj, option=orjson.OPT_NON_STR_KEYS)

def _json_loads(data: Union[bytes, str]) -> Any:
    return orjson.loads(data)

# --- Configuration ---
DEFAULT_BASE_URL = "http://127.0.0.1:8000"
# DEFAULT_BASE_URL = "https://torin-backend-long-waterfall-3317.fly.dev"

DEFAULT_SOCKET_HOST = "127.0.0.1"
DEFAULT_SOCKET_PORT = 8002
DEFAULT_BATCH_SIZE = 400
DEFAULT_PROCESSING_INTERVAL = 0.01
SOCKET_TIMEOUT = 10
SOCKET_RETRY_DELAY = 1
SOCKET_CONNECT_RETRIES = 5

# --- Global State ---
_current_run = None
_service_process = None
_shutdown_event = threading.Event()
_client_socket = None
_is_disabled = False
_pending_logs_queue = queue.Queue()
_flush_complete = threading.Event()
_background_thread_exception = None

# --- Logging Setup ---
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("torin_lite_client")
service_logger = logging.getLogger("torin_lite_service")

# --- Exceptions ---
class TorinLiteError(Exception):
    """Base exception for torin_lite."""
    pass

# --- Config Class ---
class Config:
    """Simple config object that behaves like both a dict and an object with attributes."""
    
    def __init__(self, config_dict: Optional[Dict[str, Any]] = None):
        self._items = dict(config_dict or {})

    def __setitem__(self, key: str, val: Any):
        self._items[key] = val

    def __getitem__(self, key: str) -> Any:
        return self._items[key]

    def __getattr__(self, key: str) -> Any:
        try:
            return self.__getitem__(key)
        except KeyError as e:
            raise AttributeError(f"'Config' object has no attribute '{key}'") from e

    def __setattr__(self, key: str, val: Any):
        if key == "_items":
            object.__setattr__(self, key, val)
        else:
            self.__setitem__(key, val)

    def update(self, d: Dict[str, Any]):
        self._items.update(d)

    def keys(self):
        return self._items.keys()

    def items(self):
        return self._items.items()

    def as_dict(self) -> Dict[str, Any]:
        return dict(self._items)

    def __repr__(self) -> str:
        return f"Config({self._items})"

# --- Socket Client ---
class SocketClient:
    """Thread-safe socket client with length-prefix framing for message passing."""
    
    _HEADER_FORMAT = ">I"  # big-endian unsigned integer (4 bytes)
    _HEADER_SIZE = struct.calcsize(_HEADER_FORMAT)

    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.sock = None
        self.connected = False
        self.send_lock = threading.Lock()
        self._buffer = bytearray()

    def connect(self, retries=SOCKET_CONNECT_RETRIES, timeout=SOCKET_TIMEOUT):
        """Connect to the socket server with retries."""
        for attempt in range(retries):
            try:
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.sock.settimeout(timeout)
                self.sock.connect((self.host, self.port))
                self.sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
                self.connected = True
                logger.info(f"Connected to service at {self.host}:{self.port}")
                return True
            except (socket.error, socket.timeout) as e:
                if self.sock:
                    self.sock.close()
                    self.sock = None
                logger.warning(f"Connection attempt {attempt+1}/{retries} failed: {e}")
                if attempt < retries - 1:
                    time.sleep(SOCKET_RETRY_DELAY * (attempt + 1))
                    
        logger.error(f"Failed to connect after {retries} attempts")
        return False

    def _send_raw(self, data: bytes) -> bool:
        """Send raw bytes over the socket."""
        if not self.connected or not self.sock:
            logger.error("Cannot send: not connected")
            return False
            
        try:
            self.sock.sendall(data)
            return True
        except (socket.error, socket.timeout) as e:
            logger.error(f"Send failed: {e}")
            self._handle_send_error()
            return False
        except Exception as e:
            logger.error(f"Unexpected send error: {e}", exc_info=True)
            self._handle_send_error()
            return False

    def _handle_send_error(self):
        """Clean up after a send error."""
        self.connected = False
        if self.sock:
            try:
                self.sock.close()
            except Exception:
                pass
            self.sock = None

    def send_message(self, message: Dict[str, Any]) -> bool:
        """Serialize and send a single message with length prefix."""
        with self.send_lock:
            try:
                message_bytes = _json_dumps(message)
                header = struct.pack(self._HEADER_FORMAT, len(message_bytes))
                if not self._send_raw(header): return False
                if not self._send_raw(message_bytes): return False
                return True
            except Exception as e:
                logger.error(f"Message send error: {e}", exc_info=True)
                self._handle_send_error()
                return False

    def send_serialized_batch(self, batch_payload: bytes) -> bool:
        """Send a pre-serialized batch with length prefix."""
        with self.send_lock:
            try:
                header = struct.pack(self._HEADER_FORMAT, len(batch_payload))
                if not self._send_raw(header): return False
                if not self._send_raw(batch_payload): return False
                return True
            except Exception as e:
                logger.error(f"Batch send error: {e}", exc_info=True)
                self._handle_send_error()
                return False

    def receive_message(self) -> Optional[Dict[str, Any]]:
        """Receive a single length-prefixed message (blocking)."""
        if not self.connected or not self.sock:
            logger.error("Cannot receive: not connected")
            return None

        # Read header to get message length
        header_data = bytearray()
        while len(header_data) < self._HEADER_SIZE:
            try:
                chunk = self.sock.recv(self._HEADER_SIZE - len(header_data))
                if not chunk:
                    logger.info("Connection closed by peer")
                    self._handle_send_error()
                    return None
                header_data.extend(chunk)
            except socket.timeout:
                logger.warning("Header receive timeout")
                return None
            except socket.error as e:
                logger.error(f"Header receive error: {e}")
                self._handle_send_error()
                return None

        try:
            message_length = struct.unpack(self._HEADER_FORMAT, header_data)[0]
        except struct.error as e:
            logger.error(f"Invalid header: {e}. Data: {header_data!r}")
            self._handle_send_error()
            return None

        # Read the full message body
        message_data = bytearray()
        while len(message_data) < message_length:
            bytes_to_read = min(4096, message_length - len(message_data))
            try:
                chunk = self.sock.recv(bytes_to_read)
                if not chunk:
                    logger.error("Connection closed while reading message")
                    self._handle_send_error()
                    return None
                message_data.extend(chunk)
            except socket.timeout:
                logger.warning("Message body timeout")
                return None
            except socket.error as e:
                logger.error(f"Message body receive error: {e}")
                self._handle_send_error()
                return None

        # Deserialize the message
        try:
            return _json_loads(message_data)
        except Exception as e:
            logger.error(f"Message deserialization failed: {e}", exc_info=True)
            return None

    def close(self):
        """Close the socket connection."""
        if self.sock:
            try:
                self.sock.close()
            except socket.error as e:
                logger.error(f"Socket close error: {e}")
            finally:
                self.sock = None
                self.connected = False

# --- Log Processor ---
class LogProcessor(threading.Thread):
    """Process and send log messages in batches."""
    
    def __init__(
        self,
        socket_client,
        flush_event,
        batch_size=DEFAULT_BATCH_SIZE,
        processing_interval=DEFAULT_PROCESSING_INTERVAL,
    ):
        super().__init__(daemon=True, name="LogProcessor")
        self.socket_client = socket_client
        self.queue = _pending_logs_queue
        self.flush_event = flush_event
        self.stopping = False
        self.batch_size = max(1, batch_size)
        self.processing_interval = processing_interval
        self.processed_count = 0
        self.total_batches_sent = 0
        self.last_stats_time = time.time()
        self.stats_interval = 10  # Log stats every 10 seconds

    def run(self):
        """Main processing loop."""
        try:
            logger.info(f"Log processor started (batch size={self.batch_size}, interval={self.processing_interval}s)")
            
            while not self.stopping:
                processed_this_cycle = self._process_batch()

                # Sleep only if nothing was processed
                if processed_this_cycle == 0:
                    # Wait for interval OR flush request OR stop signal
                    triggered = self.flush_event.wait(timeout=self.processing_interval)
                    if triggered:
                        self._handle_flush_request()
                    elif self.stopping:
                        break
                else:
                    # Check for flush request after processing
                    if self.flush_event.is_set():
                        self._handle_flush_request()

                self._maybe_log_stats()

        except Exception as e:
            global _background_thread_exception
            _background_thread_exception = e
            logger.error(f"Log processor error: {e}", exc_info=True)
        finally:
            try:
                self._flush_remaining()
            except Exception as e:
                logger.error(f"Final flush error: {e}", exc_info=True)

            logger.info(f"Log processor exiting (processed={self.processed_count}, batches={self.total_batches_sent})")

    def _maybe_log_stats(self):
        """Log processing statistics periodically."""
        now = time.time()
        if now - self.last_stats_time > self.stats_interval:
            qsize = self.queue.qsize()
            if qsize > 0 or self.processed_count > 0:
                logger.info(f"Stats: queue={qsize}, processed={self.processed_count}, batches={self.total_batches_sent}")
            self.last_stats_time = now

    def _process_batch(self):
        """Process a batch of messages from the queue."""
        batch = []
        try:
            # Get up to batch_size messages
            for _ in range(self.batch_size):
                message = self.queue.get_nowait()
                if message is None:  # Shutdown signal
                    self.stopping = True
                    self.queue.put(None)  # Put signal back for potential final flush
                    self.queue.task_done()
                    return 0
                batch.append(message)
                self.queue.task_done()
        except queue.Empty:
            pass  # Normal when queue is empty

        if not batch:
            return 0

        # Serialize the batch
        try:
            batch_payload = _json_dumps(batch)
        except Exception as e:
            logger.error(f"Batch serialization failed: {e}", exc_info=True)
            # Requeue failed items
            for msg in batch:
                self.queue.put(msg)
            return 0

        # Send the batch
        if self.socket_client.send_serialized_batch(batch_payload):
            self.processed_count += len(batch)
            self.total_batches_sent += 1
            return len(batch)
        else:
            # Requeue on send failure
            logger.warning(f"Requeuing {len(batch)} messages after send failure")
            for msg in batch:
                self.queue.put(msg)
            time.sleep(0.1)  # Small delay to prevent tight loops
            return 0

    def _handle_flush_request(self):
        """Process all pending messages on flush request."""
        logger.info("Flush requested - processing all pending messages")
        start_time = time.time()
        initial_queue_size = self.queue.qsize()
        processed_during_flush = 0

        # Process until queue empty or stopping signal
        while not self.queue.empty() and not self.stopping:
            batch_processed = self._process_batch()
            processed_during_flush += batch_processed
            
            # Break on persistent failure
            if batch_processed == 0 and not self.queue.empty():
                logger.warning("Stopping flush due to persistent send failure")
                break

            # Log progress for large queues
            if initial_queue_size > 1000 and processed_during_flush % 1000 < self.batch_size:
                remaining = self.queue.qsize()
                percent = (processed_during_flush/initial_queue_size)*100
                logger.info(f"Flush progress: {processed_during_flush}/{initial_queue_size} ({percent:.1f}%). Remaining: {remaining}")

        duration = time.time() - start_time
        logger.info(f"Flush complete in {duration:.2f}s: {processed_during_flush} messages processed")

        # Signal completion and clear event
        _flush_complete.set()
        self.flush_event.clear()

    def _flush_remaining(self):
        """Final flush before thread exit."""
        remaining = self.queue.qsize()
        
        # Remove sentinel if present
        try:
            if self.queue.queue[0] is None:
                self.queue.get_nowait()
                self.queue.task_done()
                remaining -= 1
        except (IndexError, queue.Empty):
            pass  # Queue empty or None wasn't first

        if remaining > 0:
            logger.info(f"Final flush: processing {remaining} remaining messages")
            while not self.queue.empty():
                if self.stopping:
                    logger.warning("Stopping final flush due to stopping signal")
                    break
                if self._process_batch() == 0 and not self.queue.empty():
                    logger.warning("Stopping final flush due to persistent send failure")
                    break

            logger.info(f"Final flush complete. Total processed: {self.processed_count}")

    def stop(self):
        """Stop the processor thread."""
        if self.stopping:
            return

        logger.info("Stopping log processor thread...")
        self.stopping = True
        # Signal with None sentinel
        self.queue.put(None)
        # Join with timeout
        self.join(timeout=15)
        if self.is_alive():
            logger.warning(f"Log processor did not exit cleanly. Remaining queue: {self.queue.qsize()}")
        else:
            logger.info("Log processor stopped")

# --- Run Class ---
class Run:
    """Run object that interacts with the service process."""

    def __init__(
        self,
        run_id: str,
        config: Optional[Dict[str, Any]] = None,
        name: Optional[str] = None,
        project: Optional[str] = None,
        entity: Optional[str] = None,
        socket_client: Optional[SocketClient] = None,
        log_processor: Optional[LogProcessor] = None,
    ):
        self.id = run_id
        self.name = name
        self.project = project
        self.entity = entity
        self.config = Config(config)
        self._step = 0
        self._socket_client = socket_client
        self._log_processor = log_processor
        self._finished = False
        # For rate limiting logs to console
        self._last_log_print = 0
        self._log_print_interval = 5.0  # seconds

    def log(
        self,
        data: Dict[str, Any],
        step: Optional[int] = None,
        commit: bool = True,
    ):
        """Queue log metrics to be sent to the service."""
        if self._finished:
            logger.warning("Run already finished. Skipping log.")
            return

        if step is not None:
            self._step = step
        # Only increment step if not provided AND commit is True
        elif commit:
            self._step += 1

        payload = {"_step": self._step, "_timestamp": time.time(), **data}
        message = {"command": "log", "run_id": self.id, "data": payload}

        # Add to queue
        _pending_logs_queue.put(message)

        # Rate limit console logs
        now = time.time()
        if now - self._last_log_print >= self._log_print_interval:
            qsize = _pending_logs_queue.qsize()
            if qsize > 10 or self._last_log_print == 0:
                logger.info(f"Logging step {self._step}, queue size: {qsize}")
                self._last_log_print = now

        # Check for background thread errors periodically
        if self._step % 100 == 0:
            global _background_thread_exception
            if _background_thread_exception:
                err = _background_thread_exception
                _background_thread_exception = None  # Clear after raising
                raise TorinLiteError(f"Background thread failed: {err}")

    def finish(self, exit_code: Optional[int] = 0, flush_timeout=30):
        """Finish the run after flushing logs."""
        global _current_run

        if self._finished:
            return

        logger.info(f"Finishing run {self.id} (exit_code={exit_code})")

        # Flush logs with timeout
        flush_success = self._flush_logs(timeout=flush_timeout)
        if not flush_success:
            logger.warning(f"Flush timed out after {flush_timeout}s - some logs may not have been sent")

        self._finished = True

        if not self._socket_client or not self._socket_client.connected:
            logger.error(f"Socket connection not available for finishing run {self.id}")
            # Stop processor anyway
            if self._log_processor:
                logger.info(f"Stopping log processor for run {self.id}")
                self._log_processor.stop()
            if _current_run is self:
                _current_run = None
            return

        # Send finish message
        message = {
            "command": "finish",
            "run_id": self.id,
            "data": {"exit_code": exit_code},
        }

        try:
            logger.info(f"Sending finish command for run {self.id}")
            self._socket_client.send_message(message)
        except Exception as e:
            logger.error(f"Failed to send finish message: {e}", exc_info=True)
        finally:
            # Stop processor
            if self._log_processor:
                logger.info(f"Stopping log processor for run {self.id}")
                self._log_processor.stop()

            # Close socket
            if self._socket_client:
                try:
                    self._socket_client.send_message({"command": "shutdown"})
                except Exception:
                    logger.warning("Failed to send shutdown command")
                self._socket_client.close()

            if _current_run is self:
                _current_run = None

            logger.info(f"Run {self.id} finished cleanup")

    def _flush_logs(self, timeout=30):
        """Flush pending logs before finishing."""
        if _pending_logs_queue.empty():
            logger.debug(f"Flush called for run {self.id}, but queue is empty")
            return True

        queue_size = _pending_logs_queue.qsize()
        logger.info(f"Flushing {queue_size} pending logs for run {self.id}")

        # Signal flush
        _flush_complete.clear()
        _flush_request_event = threading.Event()
        _flush_request_event.set()

        # Wait with progress updates
        start_time = time.time()
        logger.info(f"Waiting up to {timeout} seconds for logs to flush...")

        while time.time() - start_time < timeout:
            if _flush_complete.wait(timeout=0.5):
                remaining = _pending_logs_queue.qsize()
                processed = queue_size - remaining
                logger.info(f"Flush complete! Processed {processed} messages")
                return True

            # Report progress every ~5 seconds
            if (time.time() - start_time) % 5 < 0.5:
                remaining = _pending_logs_queue.qsize()
                processed = queue_size - remaining
                percent = (processed/queue_size)*100
                logger.info(f"Flush in progress... {processed}/{queue_size} ({percent:.1f}%). Remaining: {remaining}")

        # Timeout occurred
        remaining = _pending_logs_queue.qsize()
        processed = queue_size - remaining
        percent = (processed/queue_size)*100
        logger.warning(f"Flush timed out after {timeout}s. {processed}/{queue_size} ({percent:.1f}%). Remaining: {remaining}")
        return False

    # Context Manager
    def __enter__(self) -> "Run":
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None:
        exit_code = 0 if exc_type is None else 1
        self.finish(exit_code=exit_code)

# --- Socket Server Worker ---

# Shared session and buffer for service worker
_service_session = requests.Session()
client_buffers: Dict[Any, bytearray] = {}

def handle_client_connection(selector, key, mask, base_url, session):
    """Handle client connection with length-prefix framing."""
    sock = key.fileobj
    client_addr = key.data

    # Get or create buffer
    if client_addr not in client_buffers:
        client_buffers[client_addr] = bytearray()
    buffer = client_buffers[client_addr]

    try:
        data = sock.recv(4096)
        if not data:
            # Client closed connection
            service_logger.info(f"Client {client_addr} disconnected")
            selector.unregister(sock)
            sock.close()
            if client_addr in client_buffers:
                del client_buffers[client_addr]
            return None

        buffer.extend(data)

        # Process complete messages
        while len(buffer) >= SocketClient._HEADER_SIZE:
            # Read header
            header_bytes = buffer[:SocketClient._HEADER_SIZE]
            try:
                message_length = struct.unpack(SocketClient._HEADER_FORMAT, header_bytes)[0]
            except struct.error as e:
                service_logger.error(f"Invalid header from {client_addr}: {header_bytes!r}. Error: {e}")
                selector.unregister(sock)
                sock.close()
                if client_addr in client_buffers:
                    del client_buffers[client_addr]
                return None

            # Check if full message is available
            full_message_size = SocketClient._HEADER_SIZE + message_length
            if len(buffer) < full_message_size:
                break  # Need more data

            # Extract and process message
            message_bytes = buffer[SocketClient._HEADER_SIZE:full_message_size]
            try:
                message = _json_loads(message_bytes)
                # Process batch or single message
                if isinstance(message, list):
                    for single_msg in message:
                        result = process_message(single_msg, base_url, session)
                        if result == "shutdown":
                            return "shutdown"
                else:
                    result = process_message(message, base_url, session)
                    if result == "shutdown":
                        return "shutdown"
            except Exception as e:
                service_logger.error(f"Error processing message from {client_addr}: {e}", exc_info=True)

            # Remove processed message
            buffer[:] = buffer[full_message_size:]

        return None  # Continue processing

    except BlockingIOError:
        # Normal for non-blocking sockets
        pass
    except Exception as e:
        service_logger.error(f"Client connection error from {client_addr}: {e}", exc_info=True)
        try:
            selector.unregister(sock)
            sock.close()
            if client_addr in client_buffers:
                del client_buffers[client_addr]
        except Exception:
            pass
        return None

# API Batching Parameters
API_BATCH_SIZE = 100
API_FLUSH_INTERVAL = 1.0

# Storage for pending API requests
_pending_api_logs = {}  # run_id -> [logs]
_last_api_flush_time = {}  # run_id -> timestamp
_api_flush_lock = threading.Lock()

def flush_api_logs(run_id, base_url, session, force=False):
    """Flush pending logs for a run to the API server."""
    with _api_flush_lock:
        # Skip if no logs for this run
        if run_id not in _pending_api_logs or not _pending_api_logs[run_id]:
            return False
        
        # Check if time to flush
        current_time = time.time()
        last_flush = _last_api_flush_time.get(run_id, 0)
        batch_size = len(_pending_api_logs[run_id])
        
        should_flush = (
            force or  # Force flush
            batch_size >= API_BATCH_SIZE or  # Size threshold
            (current_time - last_flush) >= API_FLUSH_INTERVAL  # Time threshold
        )
        
        if not should_flush:
            return False
        
        # Get and clear pending logs
        logs_to_send = _pending_api_logs[run_id]
        _pending_api_logs[run_id] = []
        _last_api_flush_time[run_id] = current_time
    
    # Send batch to API
    api_url = f"{base_url}/api/runs/{run_id}/history/batch"
    try:
        batch_payload = {"batch": logs_to_send}
        
        # Log for large batches
        if len(logs_to_send) > 10:
            service_logger.info(f"Sending batch of {len(logs_to_send)} logs for run {run_id}")
        
        response = session.post(api_url, json=batch_payload, timeout=30)
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException as e:
        service_logger.error(f"Batch send failed ({len(logs_to_send)} logs) for run {run_id}: {e}")
        # Return logs to queue
        with _api_flush_lock:
            _pending_api_logs.setdefault(run_id, []).extend(logs_to_send)
        return False

def process_message(message, base_url, session):
    """Process a single message from the client."""
    command = message.get("command")
    run_id = message.get("run_id")
    data = message.get("data", {})

    try:
        if command == "shutdown":
            # Flush all pending logs before shutdown
            runs_to_flush = list(_pending_api_logs.keys())
            for run_id_to_flush in runs_to_flush:
                flush_api_logs(run_id_to_flush, base_url, session, force=True)
            service_logger.info("Received shutdown command")
            return "shutdown"

        elif command == "init":
            service_logger.info(f"Service now handling run: {run_id}")
            # Initialize batching structures
            with _api_flush_lock:
                _pending_api_logs[run_id] = []
                _last_api_flush_time[run_id] = time.time()
            
            # Send init immediately
            api_url = f"{base_url}/api/runs/{run_id}/init"
            try:
                if data:
                    response = session.post(api_url, json=data, timeout=15)
                    response.raise_for_status()
            except requests.exceptions.RequestException as e:
                service_logger.error(f"Failed to initialize run {run_id}: {e}")

        elif command == "log":
            if not run_id:
                service_logger.error("Log command received without run_id")
                return None
            
            # Add to pending batch
            with _api_flush_lock:
                _pending_api_logs.setdefault(run_id, []).append(data)
                
                # Initialize flush time if not set
                if run_id not in _last_api_flush_time:
                    _last_api_flush_time[run_id] = time.time()
            
            # Check if we should flush
            flush_api_logs(run_id, base_url, session)

        elif command == "finish":
            if not run_id:
                service_logger.error("Finish command received without run_id")
                return None

            # Force flush logs
            flush_api_logs(run_id, base_url, session, force=True)
            
            # Send finish request
            api_url = f"{base_url}/api/runs/{run_id}/finish"
            try:
                response = session.put(api_url, json=data, timeout=30)
                response.raise_for_status()
                service_logger.info(f"Run {run_id} marked finished")
            except requests.exceptions.RequestException as e:
                service_logger.error(f"Failed to finish run {run_id}: {e}")
            
            # Clean up batching state
            with _api_flush_lock:
                if run_id in _pending_api_logs:
                    del _pending_api_logs[run_id]
                if run_id in _last_api_flush_time:
                    del _last_api_flush_time[run_id]
        else:
            service_logger.warning(f"Unknown command: {command}")

        return None  # Continue processing

    except Exception as e:
        service_logger.error(f"Message processing error: {e}", exc_info=True)
        return None

def _torin_service_worker(host, port, base_url):
    """Socket server thread using length-prefix framing."""
    service_logger.info(f"Starting socket server on {host}:{port}")

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        server.bind((host, port))
        server.listen(5)
        server.setblocking(False)

        selector = selectors.DefaultSelector()
        selector.register(server, selectors.EVENT_READ, data=None)

        service_logger.info("Socket server started, waiting for connections...")
        
        # Periodic flush timer
        last_periodic_flush = time.time()
        PERIODIC_FLUSH_INTERVAL = 0.5  # Check every 0.5 seconds

        while not _shutdown_event.is_set():
            # Handle socket events with timeout
            events = selector.select(timeout=0.2)
            for key, mask in events:
                if key.data is None:
                    # Accept new connection
                    client_socket, addr = server.accept()
                    client_socket.setblocking(False)
                    service_logger.info(f"Accepted connection from {addr}")
                    selector.register(client_socket, selectors.EVENT_READ, data=addr)
                else:
                    # Handle data from client
                    result = handle_client_connection(selector, key, mask, base_url, _service_session)
                    if result == "shutdown":
                        service_logger.info("Socket server shutting down...")
                        _shutdown_event.set()
                        break
            
            # Periodic flush for all active runs
            current_time = time.time()
            if current_time - last_periodic_flush >= PERIODIC_FLUSH_INTERVAL:
                last_periodic_flush = current_time
                # Get runs to check
                with _api_flush_lock:
                    runs_to_check = list(_pending_api_logs.keys())
                
                for run_id_to_flush in runs_to_check:
                    # Check each run for time-based flush
                    flush_api_logs(run_id_to_flush, base_url, _service_session)
            
            if _shutdown_event.is_set():
                break

    except Exception as e:
        service_logger.error(f"Socket server error: {e}", exc_info=True)
    finally:
        # Final flush
        with _api_flush_lock:
            runs_to_flush = list(_pending_api_logs.keys())
        
        for run_id_to_flush in runs_to_flush:
            try:
                flush_api_logs(run_id_to_flush, base_url, _service_session, force=True)
            except Exception:
                pass
        
        # Clean up
        keys = list(selector.get_map().values())
        for key in keys:
            sock = key.fileobj
            selector.unregister(sock)
            try:
                sock.close()
            except Exception:
                pass
        selector.close()
        try:
            server.close()
        except Exception:
            pass
        service_logger.info("Socket server closed")

# --- Signal Handling ---
def signal_handler(signum, frame):
    """Handle signals for graceful shutdown."""
    global _current_run

    signal_name = signal.Signals(signum).name if hasattr(signal, "Signals") else str(signum)
    logger.info(f"Received signal {signal_name}, initiating graceful shutdown...")

    # Signal service worker to stop
    _shutdown_event.set()

    # Finish current run if exists
    if _current_run and not _current_run._finished:
        logger.info(f"Finishing run {_current_run.id} due to signal...")
        try:
            exit_code = 128 + signum if signum > 0 else 1
            _current_run.finish(exit_code=exit_code, flush_timeout=10)
        except Exception as e:
            logger.error(f"Error during graceful run finish: {e}", exc_info=True)

    # Wait for service thread
    if _service_process and _service_process.is_alive():
        logger.info("Waiting for service thread to exit...")
        _service_process.join(timeout=20)
        if _service_process.is_alive():
            logger.warning("Service thread did not exit cleanly")

    # Exit process
    exit_code = 128 + signum if signum > 0 else 1
    os._exit(exit_code)

# --- Core API ---
def init(
    project: Optional[str] = None,
    entity: Optional[str] = None,
    config_dict: Optional[Dict[str, Any]] = None,
    name: Optional[str] = None,
    id: Optional[str] = None,
    resume: Optional[bool] = None,
    reinit: bool = False,
    mode: Optional[str] = None,
    settings: Optional[Dict[str, Any]] = None,
) -> Optional[Run]:
    """Initialize a run with a background service process."""
    global _current_run, _service_process, _client_socket, _is_disabled, _background_thread_exception, _pending_logs_queue

    # Reset background exception state
    _background_thread_exception = None

    # Register signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    if mode == "disabled":
        logger.info("torin_lite is disabled")
        _is_disabled = True
        return None

    _is_disabled = False

    # Get configuration
    base_url = os.environ.get("TORIN_BASE_URL", DEFAULT_BASE_URL)
    host = os.environ.get("TORIN_SOCKET_HOST", DEFAULT_SOCKET_HOST)
    port = int(os.environ.get("TORIN_SOCKET_PORT", DEFAULT_SOCKET_PORT))
    batch_size = int(os.environ.get("TORIN_BATCH_SIZE", DEFAULT_BATCH_SIZE))
    processing_interval = float(os.environ.get("TORIN_PROCESSING_INTERVAL", DEFAULT_PROCESSING_INTERVAL))

    if settings:
        base_url = settings.get("base_url", base_url)
        host = settings.get("socket_host", host)
        port = int(settings.get("socket_port", port))
        batch_size = int(settings.get("batch_size", batch_size))
        processing_interval = float(settings.get("processing_interval", processing_interval))

    base_url = base_url.rstrip("/")

    if _current_run:
        if reinit:
            logger.info(f"Finishing existing run ({_current_run.id}) on reinit")
            _current_run.finish(flush_timeout=15)
            # Wait briefly
            time.sleep(1)
            _current_run = None
            _client_socket = None
            _service_process = None
            # Clear queue
            while not _pending_logs_queue.empty():
                try:
                    _pending_logs_queue.get_nowait()
                except queue.Empty:
                    break
                _pending_logs_queue.task_done()
        else:
            logger.warning(f"Run {_current_run.id} already initialized")
            return _current_run

    # Reset events
    _shutdown_event.clear()
    _flush_complete.clear()

    # Start socket server thread if needed
    if _service_process is None or not _service_process.is_alive():
        _service_process = threading.Thread(
            target=_torin_service_worker,
            args=(host, port, base_url),
            daemon=True,
            name="SocketServer",
        )
        _service_process.start()
        logger.info("Started service thread")
        time.sleep(0.5)  # Give server time to start

    # Create/reconnect socket client
    if _client_socket is None or not _client_socket.connected:
        _client_socket = SocketClient(host, port)
        if not _client_socket.connect():
            logger.error("Failed to connect to service socket")
            _shutdown_event.set()
            if _service_process and _service_process.is_alive():
                _service_process.join(timeout=5)
            _service_process = None
            raise TorinLiteError("Failed to connect to service socket")

    # Start log processor
    log_processor = LogProcessor(
        _client_socket,
        _shutdown_event,
        batch_size=batch_size,
        processing_interval=processing_interval,
    )
    log_processor.start()

    # Create or resume run
    run_id_to_use = id
    if id and resume:
        logger.info(f"Resuming run with id: {id}")
        init_message = {"command": "init", "run_id": id, "data": {"resumed": True}}
    else:
        # Create new run via backend
        api_url = f"{base_url}/api/runs"
        payload = {
            "project": project,
            "entity": entity,
            "name": name,
            "config": config_dict or {},
        }
        try:
            logger.info(f"Creating new run via {api_url}")
            response = _service_session.post(api_url, json=payload, timeout=15)
            response.raise_for_status()
            response_data = response.json()
            run_id_to_use = response_data.get("run_id")
            if not run_id_to_use:
                raise TorinLiteError("Backend did not return a run_id")
            logger.info(f"Run started with id: {run_id_to_use}")
            init_message = {"command": "init", "run_id": run_id_to_use, "data": {}}
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to initialize run: {e}", exc_info=True)
            cleanup_on_error(log_processor)
            raise TorinLiteError(f"Failed to initialize run: {e}") from e
        except (ValueError, KeyError) as e:
            logger.error(f"Failed to parse backend response: {e}", exc_info=True)
            cleanup_on_error(log_processor)
            raise TorinLiteError(f"Failed to parse backend response: {e}") from e

    # Send init message directly
    if not _client_socket.send_message(init_message):
        logger.error("Failed to send init message to service")
        cleanup_on_error(log_processor)
        raise TorinLiteError("Failed to send init message to service")

    _current_run = Run(
        run_id=run_id_to_use,
        config=config_dict,
        name=name,
        project=project,
        entity=entity,
        socket_client=_client_socket,
        log_processor=log_processor,
    )

    # Register auto-finish
    atexit.register(finish)

    return _current_run

def log(
    data: Dict[str, Any],
    step: Optional[int] = None,
    commit: bool = True,
) -> None:
    """Queue log metrics to send to service."""
    global _current_run, _background_thread_exception

    if _is_disabled:
        return

    if _background_thread_exception:
        err = _background_thread_exception
        _background_thread_exception = None
        raise TorinLiteError(f"Background thread failed: {err}")

    if not _current_run:
        raise TorinLiteError("torin.init() must be called before log()")

    _current_run.log(data, step=step, commit=commit)

def flush(timeout=30):
    """Explicitly flush pending logs."""
    if _is_disabled:
        return True

    if _current_run and not _current_run._finished:
        return _current_run._flush_logs(timeout=timeout)

    logger.debug("Flush called without active run")
    return True

def finish(exit_code: Optional[int] = 0) -> None:
    """Flush logs and finish the run."""
    global _current_run

    if _is_disabled:
        return

    if not _current_run:
        logger.debug("finish() called without active run")
        return

    # Get current run and unset global immediately
    run_to_finish = _current_run
    _current_run = None

    run_to_finish.finish(exit_code=exit_code)

def cleanup_on_error(log_processor: Optional[LogProcessor] = None):
    """Clean up resources after error."""
    global _client_socket, _service_process
    if _client_socket:
        try:
            _client_socket.send_message({"command": "shutdown"})
        except Exception:
            pass
        _client_socket.close()
        _client_socket = None
    _shutdown_event.set()
    if log_processor:
        log_processor.stop()
    if _service_process and _service_process.is_alive():
        _service_process.join(timeout=5)
    _service_process = None

# Exception handler to ensure cleanup
_original_excepthook = sys.excepthook
def _exception_cleanup_hook(exc_type, exc_value, exc_traceback):
    finish(exit_code=1)
    if _original_excepthook:
        _original_excepthook(exc_type, exc_value, exc_traceback)
sys.excepthook = _exception_cleanup_hook

# --- Example Usage ---
if __name__ == "__main__":
    # Example code for testing with basic metrics
    run = init(project="test-project", name="socket-test")
    
    # Test logging with increasing frequency
    for i in range(5):
        log({"metric": i, "squared": i*i})
        time.sleep(0.1)
    finish()