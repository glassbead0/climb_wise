# Use the official Python image from Docker Hub
# FROM gcr.io/kaggle-images/python # this took too long
FROM python:3.13-slim

# Set the working directory inside the container
WORKDIR /app

# Install common utilities
RUN apt-get update && apt-get install -y procps less vim curl wget net-tools iputils-ping graphviz build-essential cmake

# Install Python packages
COPY docker/requirements.txt docker/
RUN pip install --no-cache-dir -r docker/requirements.txt
# needed because elkai doesn't have a prebiuld wheel for this docker image (Debian)
RUN pip install elkai --no-binary elkai

# create log directory
RUN mkdir -p /app/log
RUN touch /app/log/jupyter.log
RUN chmod 777 /app/log/jupyter.log

# Copy some files into the container
COPY jupyter/start_jupyter.sh jupyter/
RUN chmod +x jupyter/start_jupyter.sh

# Copy your project files into the container
COPY . .

RUN echo "alias jc='jupyter console --existing'" >> ~/.bashrc && \
    echo "source ~/.bashrc" >> ~/.bash_profile

# Set the default command to run when the container starts
CMD ["/bin/bash"]
