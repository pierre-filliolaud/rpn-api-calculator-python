# 🧮 RPN API Calculator (Python)

This project is a REST API built with **FastAPI** that evaluates expressions written in **Reverse Polish Notation (RPN)**.  
It stores operations in a database, supports exporting results to CSV, and is containerized with Docker.

---

## 🚀 Features

- ✅ Evaluate RPN expressions (e.g. `3 4 + 2 *`)
- ✅ Store operations and results in a database
- ✅ Export data to CSV
- ✅ REST API powered by FastAPI
- ✅ Docker & Docker Compose ready

---

## 🧱 Project Structure

```
src/
└── rpn_api_calculator/
    ├── main.py           # FastAPI app
    ├── api/              # Routes
    ├── services/         # RPN logic
    ├── db/               # Database models and session
tests/                    # Pytest unit tests
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

## ▶️ Run the app locally

```bash
# Activate virtual environment
poetry shell

# Start FastAPI server
uvicorn rpn_api_calculator.main:app --reload --app-dir src
```

Access the app at: [http://localhost:8000](http://localhost:8000)  
Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🧪 Run tests

```bash
poetry run pytest --cov
```

---

## 🐳 Run with Docker

```bash
docker-compose up --build
```

---

## 📤 Export CSV

Use the API endpoint:
```
GET /export
```

---

## 🧾 License

MIT
