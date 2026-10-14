
# Start from an official Python image
FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /app

# Avoid generating .pyc files and buffer-free logging
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Copy dependency list first
COPY requirements.txt .

# Install application dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY app.py .

# Document the port used by the application
EXPOSE 8000

# Start the Flask application using Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]
