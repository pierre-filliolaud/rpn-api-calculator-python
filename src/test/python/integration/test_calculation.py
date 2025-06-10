import pytest
from fastapi.testclient import TestClient
from uuid import UUID
import os
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from rpn_api_calculator.main import app
from rpn_api_calculator.db.database import Base, get_db
from rpn_api_calculator.domain.calculation import Calculation

# Use an in-memory SQLite database for testing
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

# Create a test engine and session
engine = create_async_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# Override the get_db dependency
async def override_get_db():
    async with TestingSessionLocal() as session:
        yield session

app.dependency_overrides[get_db] = override_get_db

# Create a test client
client = TestClient(app)

# Test data
test_calculation = {
    "expression": "2 3 +",
    "result": 5.0
}

updated_calculation = {
    "expression": "2 3 *",
    "result": 6.0
}

# Setup and teardown
@pytest.fixture(scope="session", autouse=True)
def setup_database():
    # Create tables
    asyncio.run(async_setup_database())
    yield
    # Drop tables
    asyncio.run(async_teardown_database())

async def async_setup_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def async_teardown_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

# Tests
def test_create_calculation():
    response = client.post("/api/calculations/", json=test_calculation)
    assert response.status_code == 200
    data = response.json()
    assert data["expression"] == test_calculation["expression"]
    assert data["result"] == test_calculation["result"]
    assert "id" in data
    assert "created_at" in data

def test_get_calculation():
    # First create a calculation
    create_response = client.post("/api/calculations/", json=test_calculation)
    calculation_id = create_response.json()["id"]

    # Then get it
    response = client.get(f"/api/calculations/{calculation_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == calculation_id
    assert data["expression"] == test_calculation["expression"]
    assert data["result"] == test_calculation["result"]

def test_update_calculation():
    # First create a calculation
    create_response = client.post("/api/calculations/", json=test_calculation)
    calculation_id = create_response.json()["id"]

    # Then update it
    response = client.put(f"/api/calculations/{calculation_id}", json=updated_calculation)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == calculation_id
    assert data["expression"] == updated_calculation["expression"]
    assert data["result"] == updated_calculation["result"]

    # Verify the update
    get_response = client.get(f"/api/calculations/{calculation_id}")
    assert get_response.json()["expression"] == updated_calculation["expression"]

def test_delete_calculation():
    # First create a calculation
    create_response = client.post("/api/calculations/", json=test_calculation)
    calculation_id = create_response.json()["id"]

    # Then delete it
    response = client.delete(f"/api/calculations/{calculation_id}")
    assert response.status_code == 200
    assert response.json() == {"ok": True}

    # Verify it's gone
    get_response = client.get(f"/api/calculations/{calculation_id}")
    assert get_response.status_code == 404

def test_list_calculations():
    # We can't directly access the database in a synchronous test function,
    # so we'll just create new calculations and test that they appear in the list

    # Create a few calculations
    client.post("/api/calculations/", json=test_calculation)
    client.post("/api/calculations/", json=updated_calculation)

    # Get the list
    response = client.get("/api/calculations/")
    assert response.status_code == 200
    data = response.json()

    # Verify that at least our test calculations are in the list
    expressions = [calc["expression"] for calc in data]
    assert test_calculation["expression"] in expressions
    assert updated_calculation["expression"] in expressions
