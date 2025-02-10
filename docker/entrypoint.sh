#!/bin/sh
set -e

touch /app/log/jupyter.log

# Start Jupyter in the background
/app/jupyter/start_jupyter.sh &

exec tail -f /app/log/jupyter.log
