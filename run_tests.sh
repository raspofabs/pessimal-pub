#!/bin/bash

poetry install
while true; do
    # rerun script whenever anything changes in the pessimal or tests folders
    find pessimal tests | sed '/__pycache__/d' > interesting_files.txt
    cat interesting_files.txt | entr -d poetry run tests/run.sh ;
    rm interesting_files.txt
    # sleep for four seconds so we have a chance to quit
    sleep 4
done
