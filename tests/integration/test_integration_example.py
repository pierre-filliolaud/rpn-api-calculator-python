from fastapi.testclient import TestClient
from rpn_api_calculator.main import app

client = TestClient(app)

def test_api_status():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the RPN API Calculator!"}