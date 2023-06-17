# Using official python runtime base image
FROM python:3.10.5-alpine3.16

# Set the application directory
WORKDIR /app

# Install our requirements.txt
ADD requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

# Copy our code from the current folder to /app inside the container
ADD . /app

CMD ["celery", "-A", "tasks", "worker", "--loglevel=INFO"]