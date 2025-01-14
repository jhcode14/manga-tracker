# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container
COPY ./app .

# Install dependencies (assuming ./app have requirements.txt)
RUN pip install --no-cache-dir -r requirements.txt

# Copy wait-for-it script
COPY ./scripts/wait-for-it.sh /usr/src/app/
RUN chmod +x /usr/src/app/wait-for-it.sh

# Set environment variables
ENV PYTHONPATH=/usr/src/app
ENV FLASK_APP=main:server
ENV FLASK_RUN_HOST=0.0.0.0
#ENV FLASK_RUN_RELOAD=False
ENV FLASK_DEBUG=1