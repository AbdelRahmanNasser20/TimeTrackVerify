# Use an official Python runtime as a parent image
FROM python:3.10.14-slim

# Set the working directory in the container
WORKDIR /app

# Install the PostgreSQL client and development libraries
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev

RUN apt-get update && apt-get install -y postgresql-client

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

RUN pip install gunicorn


# Copy the rest of the application code into the container
COPY . .

# Copy the rest of the application code into the container
COPY . /app

# Expose the port your application runs on
EXPOSE 5001

ENV FLASK_ENV=production


# Run the Flask app and then the test script
# CMD ["sh", "-c", "python run.py & sleep 5 && python /app/test_script.py"]
CMD ["gunicorn","-b", "0.0.0.0:5001", "run:app"]

