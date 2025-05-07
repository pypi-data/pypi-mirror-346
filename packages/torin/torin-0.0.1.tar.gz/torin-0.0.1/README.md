# Torin

A lightweight Python package for logging and tracking metrics.

## Installation

```bash
pip install torin
```

## Usage

```python
import torin

# Initialize a run
run = torin.init(project="my-project", name="experiment-1")

# Log metrics
torin.log({"accuracy": 0.95, "loss": 0.05})

# Finish the run
torin.finish()
```

## API Reference

### `torin.init()`

Initializes a run and connects to the backend service.

```python
run = torin.init(
    project="my-project",
    entity="my-team",
    name="experiment-1",
    config_dict={"learning_rate": 0.01}
)
```

### `torin.log()`

Logs metrics or other data to the current run.

```python
torin.log(
    {"accuracy": 0.95, "loss": 0.05},
    step=10,
    commit=True
)
```

### `torin.finish()`

Flushes all pending logs and finishes the run.

```python
torin.finish(exit_code=0)
```

### `torin.flush()`

Explicitly flushes pending logs.

```python
torin.flush(timeout=30)
```

## License

[MIT License](LICENSE)