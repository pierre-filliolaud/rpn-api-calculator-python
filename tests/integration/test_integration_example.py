import requests
import pytest

# Exemple de test d'intégration

def test_api_status():
    response = requests.get('http://localhost:8000/')  # Assurez-vous que l'API est en cours d'exécution
    assert response.status_code == 200
