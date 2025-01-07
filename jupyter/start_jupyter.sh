#!/bin/bash
# Start Jupyter Notebook
jupyter notebook --ip=0.0.0.0 --port=8887 --no-browser --allow-root --NotebookApp.token='' > /app/log/jupyter.log 2>&1 &

# Wait for the Jupyter server to start
sleep 5

# Start a new kernel to create the kernel connection file
jupyter kernel > /dev/null 2>&1 &

# Print the location of the kernel connection file
echo "Kernel connection files are located in: $(jupyter --runtime-dir)"
