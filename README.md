# 🧮 RPN API Calculator (Python)

This project is a REST API built with **FastAPI** that evaluates expressions written in **Reverse Polish Notation (RPN)**.  
It stores operations in a database, supports exporting results to CSV, and is containerized with Docker.

---

## 🚀 Features

- ✅ Evaluate RPN expressions (e.g. `3 4 + 2 *`)
- ✅ Store operations and results in a database
- ✅ Export data to CSV
- ✅ REST API powered by FastAPI
- ✅ React UI for easy interaction
- ✅ Docker & Docker Compose ready

---

## 🧱 Project Structure

```
src/
├── main/
│   ├── python/
│   │   └── rpn_api_calculator/
│   │       ├── main.py           # FastAPI app
│   │       ├── api/              # Routes
│   │       ├── service/          # Business logic
│   │       └── db/               # Database models and session
│   ├── docker/                   # Docker configuration
│   └── webapp/                   # React UI
│       ├── public/               # Static files
│       └── src/                  # React components
└── test/
    └── python/                   # Pytest unit and integration tests
```

---

## ⚙️ Installation

```bash
# Clone the repository
git clone https://github.com/your-username/rpn-api-calculator-python.git
cd rpn-api-calculator-python

# Install dependencies
poetry install
```

---

## ▶️ Run the app locally (dev mode)

### Backend API

```bash
# Activate virtual environment
poetry shell

# Start FastAPI server
uvicorn rpn_api_calculator.main:app --reload --app-dir src
```

Then open:  
📍 [http://localhost:8000](http://localhost:8000)  
📚 Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)

### React UI

```bash
# Navigate to the webapp directory
cd src/main/webapp

# Install dependencies
npm install

# Start the development server
npm start
```

Then open:  
🖥️ [http://localhost:3000](http://localhost:3000)

---

## 🧪 Run tests

```bash
poetry run pytest --cov
```

---

## 🐳 Run the app with Docker (standalone)

Build and run the container:
```bash
docker build -f ./src/main/docker/Dockerfile -t rpn-api-calculator .
docker run -p 8000:8000 rpn-api-calculator
```

---

## 🐙 Run with Docker Compose (dev mode)

Launch with live reload and volume mount:

```bash
docker-compose -f src/main/docker/docker-compose.yml up --build
```

Then open in browser:
- App: [http://localhost:8000](http://localhost:8000)
- Docs: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🐙 Run with Docker Compose (production mode)

Launch the complete application with API and PostgreSQL database:

```bash
docker-compose -f src/main/docker/app.yml up
```

This will:
- Start the API service using the Docker image
- Start the PostgreSQL database
- Set up the necessary environment variables and networking between services

Then open in browser:
- App: [http://localhost:8000](http://localhost:8000)
- Docs: [http://localhost:8000/docs](http://localhost:8000/docs)

---

### 📦 docker-compose.yml (reference)

```yaml
version: '3.8'

services:
  app:
    build:
      context: .
      dockerfile: src/main/docker/Dockerfile
    ports:
      - "8000:8000"
    environment:
      - ENVIRONMENT=development
    volumes:
      - .:/app
    command: uvicorn src.rpn_api_calculator.main:app --host 0.0.0.0 --port 8000 --reload
```

✅ This setup mounts the local code into the container and uses `--reload` for development hot reload.

### 📦 app.yml (reference)

```yaml
version: '3.8'

services:
  rpn-api:
    build:
      context: ../../..
      dockerfile: ./src/main/docker/Dockerfile
    ports:
      - "8000:8000"
    environment:
      - ENVIRONMENT=production
      - DATABASE_URL=postgresql+asyncpg://rpn:rpn@rpn-postgresql:5432/rpn_db
    depends_on:
      - rpn-postgresql
    networks:
      - rpn-network

  rpn-postgresql:
    image: postgres:14.2
    container_name: rpn-postgresql
    environment:
      POSTGRES_USER: rpn
      POSTGRES_PASSWORD: rpn
      POSTGRES_DB: rpn_db
    ports:
      - "5432:5432"
    volumes:
      - postgres-data:/var/lib/postgresql/data
    networks:
      - rpn-network

networks:
  rpn-network:
    driver: bridge

volumes:
  postgres-data:
```

✅ This setup runs both the API and PostgreSQL database in production mode with proper networking and data persistence.

---

## 📤 Export CSV

To get all saved operations and results as CSV, call:

```
GET /export
```

---

## 💻 React UI

The project includes a web-based React UI for interacting with the RPN Calculator API:

### Features

- Simple, intuitive interface for entering RPN expressions
- Real-time validation and error handling
- Responsive design with Tailwind CSS
- Displays calculation results

### How it works

1. User enters an RPN expression (e.g., "3 4 +")
2. The expression is validated and evaluated locally
3. The expression and result are sent to the API
4. The result is displayed to the user

### API Integration

The UI makes POST requests to the `/api/calculations/` endpoint with the following payload:

```json
{
  "expression": "3 4 +",
  "result": 7
}
```

For more details, see the [webapp README](src/main/webapp/README.md).

---
