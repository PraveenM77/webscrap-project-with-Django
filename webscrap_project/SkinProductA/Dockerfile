# Use the official Python 3.8 slim image from Docker Hub
FROM python:3.8-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app/

# Install the necessary dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt  # Make sure your requirements.txt contains necessary libraries, including psycopg2, scrapy, etc.

# Expose any ports if required (e.g., for the Scrapy web app)
EXPOSE 8000

# Command to run your scraper or Python script
CMD ["python", "pushToElasticsearch.py"]
