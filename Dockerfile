# Use Python 3.11 Alpine base image
FROM python:3.11.2-alpine

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install dependencies and clean up in one layer
RUN pip install --no-cache-dir -r requirements.txt && \
    rm -rf /var/cache/apk/*

# Copy the content of the local src directory to the working directory
COPY ./src .

# Install cronie (for cron jobs) and clean up in one layer
RUN apk add --no-cache cronie && \
    rm -rf /var/cache/apk/*


# Add crontab file in the cron directory and set permissions
COPY crontab /etc/cron.d/my-crontab
RUN chmod 0644 /etc/cron.d/my-crontab && \
    crontab /etc/cron.d/my-crontab

# Copy and set permissions for the entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Create the log file to be able to run tail
RUN touch /var/log/cron.log

# Set the entrypoint
ENTRYPOINT ["/bin/sh", "/entrypoint.sh"]

