
[![Python application](https://github.com/kmu/tafel/actions/workflows/test.yaml/badge.svg)](https://github.com/kmu/tafel/actions/workflows/test.yaml)
[![codecov](https://codecov.io/gh/kmu/tafel/graph/badge.svg?token=E48EGKC5FQ)](https://codecov.io/gh/kmu/tafel)

# Tafel


A command-line tool for extracting Tafel slopes from MPT files.

This tool is currently in an experimental stage.

## Supported files

- xy files: assumes simple xy format. See [here](dataset/HER.xy) for an example.
- csv files: assumes LSV experiments conducted using Hokuto. See [here](tests/data/example2.CSV) for an example.
- mpt files: assumes LSV experiments conducted using BioLogic EC-Lab. See [here](tests/data/example.mpt) for an example.

## Installation

Requirements: Python 3.11 or above

```bash
pip install tafel
```

## How to use

### Simple xy files

```
tafel -f dataset/HER.csv
```

### Bio-logic files

```bash
tafel -f path/to/file/file.mpt --reference-potential 0.210 --ph 13 --electrolyte-resistance 0.05
```

### Hokuto files

```bash
tafel -f path/to/file/file.xyz --reference-potential 0.210 --ph 13 --electrolyte-resistance 0.05
```

## For Developers

### Getting Started

To set up the development environment, run:

```bash
pdm install
```

### Code Quality Check

To check the code quality, run:

```bash
pdm run check
```

To test CLI, run

```
pdm run python src/tafel/app/cli.py -f dataset/HER.csv
```

### Release a New PyPI Package

To release a new version, update the `pyproject.toml` file with the new version number and publish a new release from [here](https://github.com/kmu/tafel/releases/new).
