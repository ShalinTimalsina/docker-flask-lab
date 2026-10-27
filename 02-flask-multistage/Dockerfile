# ==========================================
# Stage 1: Build stage (compile & install dependencies)
# ==========================================
FROM python:3.12-slim AS builder

# Set working directory for dependencies build
WORKDIR /build

# Create a dedicated virtual environment
RUN python -m venv /opt/venv

# Activate virtual environment in PATH for installation
ENV PATH="/opt/venv/bin:$PATH"

# Copy requirements and install packages inside virtual environment
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ==========================================
# Stage 2: Runtime stage (clean & lightweight)
# ==========================================
FROM python:3.12-slim AS runner

# Create a dedicated non-root user for security best practices
RUN useradd --create-home --shell /bin/bash appuser

# Set working directory for application runtime
WORKDIR /app

# Copy the prepared virtual environment from builder stage
COPY --from=builder /opt/venv /opt/venv

# Add virtual environment binaries to PATH
ENV PATH="/opt/venv/bin:$PATH"

# Copy application source code
COPY app.py .

# Give the non-root user ownership of the application directory
RUN chown -R appuser:appuser /app

# Switch from root to unprivileged user
USER appuser

# Expose port 5000 for HTTP traffic
EXPOSE 5000

# Run the app with production WSGI server Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "app:app"]
