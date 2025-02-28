# Use the official Python 3.8 slim image from Docker Hub
FROM python:3.8-slim

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies (gcc, libc-dev, build-essential, libpq-dev, etc.)
RUN apt-get update && apt-get install -y \
    gcc \
    libc-dev \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy the current directory contents into the container at /app
COPY . /app/

# Upgrade pip and install the Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt  # Make sure your requirements.txt contains necessary libraries, including psycopg2, scrapy, etc.

# Expose any ports if required (e.g., for the Scrapy web app)
EXPOSE 8000

# Command to run your scraper or Python script
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
