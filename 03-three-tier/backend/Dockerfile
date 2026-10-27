# ==========================================
# Stage 1: Build stage (compile & install dependencies)
# ==========================================
FROM python:3.12-slim AS builder

# Set working directory for dependencies build
WORKDIR /build

# Create a clean virtual environment
RUN python -m venv /opt/venv

# Activate virtual environment in PATH
ENV PATH="/opt/venv/bin:$PATH"

# Copy dependencies list and install packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ==========================================
# Stage 2: Runtime stage (production WSGI server)
# ==========================================
FROM python:3.12-slim AS runner

# Create a dedicated non-root user for security
RUN useradd --create-home --shell /bin/bash appuser

# Set working directory for the application
WORKDIR /app

# Copy virtual environment from builder stage
COPY --from=builder /opt/venv /opt/venv

# Set PATH to use the virtual environment
ENV PATH="/opt/venv/bin:$PATH"

# Copy application source code
COPY app.py .

# Grant ownership to non-root user
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Expose backend port 5000
EXPOSE 5000

# Start Gunicorn WSGI server with 2 worker processes
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "app:app"]
