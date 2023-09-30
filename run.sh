#!/bin/sh
export FLASK_APP=main
export FLASK_ENV=development
export FLASK_DEBUG=True
export FLASK_RUN_PORT=8040
python3 -m flask run
