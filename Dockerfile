# Use Python 3.11.2 base image
FROM python:3.11.2

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install any dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the content of the local src directory to the working directory
COPY . .

# Install cron
RUN apt-get update && apt-get -y install cron

# Add crontab file in the cron directory
ADD crontab /etc/cron.d/my-crontab

# Give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/my-crontab

# Apply cron job
RUN crontab /etc/cron.d/my-crontab

# Create the log file to be able to run tail
RUN touch /var/log/cron.log

# Run the command on container startup
CMD cron && tail -f /var/log/cron.log
