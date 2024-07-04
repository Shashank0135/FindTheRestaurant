FROM python:3.11

WORKDIR /code

# Copy the application code and entrypoint script
COPY . /code

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Make the entrypoint script executable
RUN chmod +x /code/entrypoint.sh

# Set the entrypoint to the custom script
ENTRYPOINT ["/code/entrypoint.sh"]
