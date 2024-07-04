#!/bin/bash

poetry install
COVERAGE_PARAMS="--cov=pessimal --no-cov-on-fail --cov-report term-missing --cov-branch --cov-report html tests/"
PYTEST_PARAMS="--durations=3"
find pessimal tests | entr poetry run pytest $PYTEST_PARAMS $COVERAGE_PARAMS ;
