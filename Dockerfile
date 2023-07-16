# Use a specific Python version (3.8-alpine)
FROM python:3.8-alpine

# Set the working directory
WORKDIR /app

# Copy the requirements file to the working directory
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Set environment variables
ENV ALEMBIC_CONFIG=/app/alembic.ini

# Expose the port
EXPOSE 8000

# Run the Alembic upgrade command and start the application
CMD alembic upgrade head && \
  uvicorn main:app --host 0.0.0.0 --port 8000
