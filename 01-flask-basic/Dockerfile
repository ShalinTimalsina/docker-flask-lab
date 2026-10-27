# Use official lightweight Python 3.12 image
FROM python:3.12-slim

# Set container working directory
WORKDIR /app

# Copy dependencies file first for Docker layer caching
COPY requirements.txt .

# Install Python dependencies without caching install wheels to save space
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code into the container
COPY app.py .

# Inform Docker that the container listens on port 5000
EXPOSE 5000

# Start the Flask development server on container startup
CMD ["python", "app.py"]
