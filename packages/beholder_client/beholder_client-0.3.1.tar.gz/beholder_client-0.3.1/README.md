# beholder-py

Python client library for [beholder](https://github.com/mbari-org/beholder).

## Build

This project is built with [Poetry](https://python-poetry.org/).

You can build the project with the following command:

```bash
poetry build
```

This will create a `dist/` directory with the built `beholder` package.

## Install

You can install the built package with the following command:

```bash
pip install dist/beholder-<VERSION>.whl
```

## Development

To configure the project for development, install Poetry and run

```bash
poetry install
poetry shell
```

This will create a virtual environment for the project, install all dependencies into it, then spawn a new shell with the environment activated.

---

&copy; Monterey Bay Aquarium Research Institute, 2022