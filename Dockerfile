# Multi-stage Dockerfile for MBTI Roster
# Stage 1: Base image with dependencies
FROM python:3.13-slim as base

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements_minimal.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements_minimal.txt

# Stage 2: Development image
FROM base as development

# Install development dependencies
RUN pip install --no-cache-dir \
    pytest \
    pytest-cov \
    pytest-asyncio \
    black \
    flake8 \
    mypy \
    bandit \
    safety \
    httpx

# Copy application code
COPY . .

# Create non-root user
RUN useradd --create-home --shell /bin/bash app && \
    chown -R app:app /app
USER app

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Development command
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# Stage 3: Production image
FROM base as production

# Install production dependencies
RUN pip install --no-cache-dir \
    gunicorn \
    uvicorn[standard]

# Copy application code
COPY . .

# Create non-root user
RUN useradd --create-home --shell /bin/bash app && \
    chown -R app:app /app
USER app

# Create necessary directories
RUN mkdir -p /app/data_uploads/pending \
    /app/data_uploads/processed \
    /app/data_uploads/failed \
    /app/logs

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Production command
CMD ["gunicorn", "app.main:app", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]

# Stage 4: Testing image
FROM development as testing

# Install testing dependencies
RUN pip install --no-cache-dir \
    locust \
    pytest-html \
    pytest-xdist

# Copy test files
COPY tests/ /app/tests/
COPY run_tests.py /app/

# Set test environment
ENV TESTING=1 \
    DATABASE_URL=sqlite:///./test_mbti_roster.db

# Test command
CMD ["pytest", "tests/", "-v", "--cov=app", "--cov-report=html", "--cov-report=term-missing"] 