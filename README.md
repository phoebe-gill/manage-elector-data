# manage-elector-data

Tools to manage elector data for the Tower Hamlets Green Party

## Pre-requisites

This project uses [poetry](https://python-poetry.org/docs/). Install poetry, and then run `poetry install`.

## Running the tools

Merge data from the Tower Hamlets Green Party into the December 2024 version of the electoral register from the council: `poetry run python towerhamlets/match.py -h`

## Development

Run formatting with `poetry run black .`.

Run linting with `poetry run flake8`.

Run tests with `poetry run pytest`.
