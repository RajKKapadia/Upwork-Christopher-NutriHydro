# Use an official Python runtime as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Flask application code into the container
COPY . .

# Expose the port that the Flask application will run on
EXPOSE 5000

# Run the Flask application when the container launches
CMD gunicorn --bind 0.0.0.0:5000 run:app
