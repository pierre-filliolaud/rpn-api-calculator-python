# Use official Python runtime as a parent image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install --upgrade pip && pip install poetry

# Copy only requirements to cache dependencies
COPY pyproject.toml poetry.lock* /app/

# Install dependencies
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi

# Copy project
COPY ./src /app/src
COPY ./README.md /app/

# Expose port
EXPOSE 8000

# Command to run the app with Uvicorn
CMD ["uvicorn", "src.rpn_api_calculator.main:app", "--host", "0.0.0.0", "--port", "8000"]
