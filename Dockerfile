# Use the official Python base image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Flask application code into the container
COPY server.py .

# Expose the port on which the Flask app runs
EXPOSE 8080

# Command to run the Flask application
CMD ["python", "server.py"]
