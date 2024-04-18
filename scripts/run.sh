#!/bin/sh
set -e

TABLES_PATH=$KBC_DATADIR/out/tables

if [ "$(ls -A $TABLES_PATH)" ]; then
    TABLES_PATH=$TABLES_PATH/*
     rm -r $TABLES_PATH
fi

python /code/src/component.py