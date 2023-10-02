# Use the official Python image as the base image
FROM python:3.8

# Set environment variables
ENV PYTHONUNBUFFERED 1

# Create and set the working directory
WORKDIR /app

# Copy the requirements file to the container's working directory
COPY requirements.txt /app/

# Install project dependencies
RUN pip install -r requirements.txt

# Copy the entire project directory to the container
COPY . /app/

# Expose the port your DRF application runs on (e.g., 8000)
EXPOSE 80

# Define the command to start the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:80"]