from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="torin",
    version="0.0.1",
    author="Akshay Vegesna",
    author_email="akshay.vegesna@gmail.com",
    description="A lightweight logging and tracking utility",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/torin-ai/torin.git",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "requests>=2.25.0",
        "orjson>=3.0.0",
    ],
)