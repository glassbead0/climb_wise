#!/bin/bash

jupyter notebook --ip=0.0.0.0 --port=8887 --no-browser --allow-root --NotebookApp.token='' > /app/log/jupyter.log 2>&1 &

tail -f /dev/null