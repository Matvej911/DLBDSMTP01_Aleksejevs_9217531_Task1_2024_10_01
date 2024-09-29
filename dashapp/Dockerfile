# Use the official Python image
FROM python:3.9-slim

# Set the working directory
WORKDIR /dashapp

# Copy the current directory contents into the container at /app
COPY requirements5.txt .

# Install the required packages
RUN pip install --no-cache-dir -r requirements5.txt


COPY dashapp.py ./

# Command to run both apps (Flask and Dash)
CMD ["python", "dashapp.py"]
