# ====================
# Builder stage
# ====================
FROM python:3.12-slim-bullseye as builder

# metadata
LABEL maintainer="Shuyib" \
      description="Regression test using data version control principles"\
      version="0.1"

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    KAGGLE_CONFIG_DIR=/home/appuser/.kaggle \
    PATH="/app/venv/bin:$PATH"

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        make \
        curl \
        libcap2-bin \
        zip \
        unzip && \
    apt-get upgrade -y && \
    rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN groupadd -r appuser && \
    useradd -r -m -g appuser appuser

# Create directory structure
WORKDIR /app
RUN mkdir -p /app/data/original_data \
            /app/data/transform \
            /app/output \
            /app/model_output \
            /home/appuser/.kaggle && \
    chown -R appuser:appuser /app /home/appuser/.kaggle && \
    chmod 700 /home/appuser/.kaggle

# Install Python dependencies
COPY --chown=appuser:appuser requirements.txt .
USER appuser
RUN python -m venv --copies /app/venv && \
    /app/venv/bin/pip install --no-cache-dir --upgrade pip && \
    /app/venv/bin/pip install --no-cache-dir -r requirements.txt

# ====================
# Final stage
# ====================
FROM python:3.12-slim-bullseye

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    KAGGLE_CONFIG_DIR=/home/appuser/.kaggle \
    PATH="/app/venv/bin:$PATH"

# Install required system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        make \
        curl \
        libcap2-bin \
        zip \
        unzip && \
    rm -rf /var/lib/apt/lists/*

# Copy user and group from builder
COPY --from=builder /etc/passwd /etc/passwd
COPY --from=builder /etc/group /etc/group

# Copy application files and set permissions
WORKDIR /app
COPY --from=builder --chown=appuser:appuser /app /app
COPY --from=builder --chown=appuser:appuser /home/appuser /home/appuser
COPY --chown=appuser:appuser . .

# Set Python capabilities and ensure directories exist
USER root
# make sure the directories exist and are owned by appuser
# this is necessary because the directories are created by the builder
#
RUN mkdir -p /app/data/original_data && \
    chown -R appuser:appuser /app && \
    setcap cap_net_bind_service=+ep /app/venv/bin/python

# Switch to non-root user
USER appuser

# Healthcheck: checks if the server is up and running
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost/ || exit 1

# Entrypoint: runs the server
CMD ["make", "all"]