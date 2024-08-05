#!/bin/bash

COVERAGE_PARAMS="--cov=pessimal --no-cov-on-fail --cov-report term-missing --cov-branch --cov-report html tests/"
PYTEST_PARAMS="--durations=3 --forked -n auto"

poetry run pytest $PYTEST_PARAMS $COVERAGE_PARAMS
