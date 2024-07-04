#!/bin/bash

poetry install
poetry run jurigged -v pessimal/main.py
