import pytest
import requests

# Test de la santé de l'API

def test_health():
    response = requests.get('http://localhost:8000/')  # Assurez-vous que l'API est en cours d'exécution
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the RPN API Calculator!"}
