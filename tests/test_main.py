from fastapi.testclient import TestClient
from app.main import app  # adjust if inside folder

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200