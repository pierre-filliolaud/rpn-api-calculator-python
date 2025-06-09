FROM python:3.10-slim

# Environment settings
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install --upgrade pip && pip install poetry

# Copy project code and metadata BEFORE install
COPY ./src/main/python /app/src/main/python
COPY pyproject.toml poetry.lock* README.md /app/

# Install dependencies
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi

# Expose port
EXPOSE 8000

# Run the app
CMD ["uvicorn", "src.rpn_api_calculator.main:app", "--host", "0.0.0.0", "--port", "8000"]