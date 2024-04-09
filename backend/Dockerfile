# This Dockerfile builds the Django backend
# It is based on the official Python 3.10-alpine image

FROM python:3.10-slim

# # Create a non-sudo user
RUN useradd -m appuser \
    && mkdir -p /app \
    && chown -R appuser:appuser /app

# Set the working directory
WORKDIR /app

# ENV APK_CACHE_DIR=/var/cache/apk
ENV APT_CACHE_DIR=/var/cache/apt/archives
ENV PIP_CACHE_DIR=/home/appuser/.cache/pip

# Install gcc and other dependencies
# Additional dependencies for Alpine Linux (use with `apk add`):
#   openblas-dev zlib-dev bzip2-dev freetype-dev harfbuzz-dev
RUN --mount=type=cache,target=${APT_CACHE_DIR} \
    # apk add --cache-dir=${APK_CACHE_DIR} \
    apt-get update && apt-get install -y \
    gcc g++ gfortran \
    musl-dev libffi-dev libpng-dev \
    postgresql-client

# Copy the requirements files
COPY --chown=appuser:appuser pyproject.toml poetry.lock ./

# Install the required Python dependencies
RUN --mount=type=cache,target=${PIP_CACHE_DIR} \
    pip install poetry \
    && poetry config virtualenvs.create false \
    && poetry install --without=dev --no-root --no-interaction --no-ansi \
    && which python && which pip

# Copy the application code
# COPY --chown=appuser:appuser . .

# Expose the port
# EXPOSE 8000

WORKDIR /app/src

# Switch to the non-sudo user
USER appuser
