from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_create_user():
    response = client.post(
        "/api/v1/User/create",
        json={
            "email": "deadpool@example.com", 
            "password": "chimichangas4life",
            "name": "Dead Pool"
            },
    )
    assert response.status_code == 201
    assert response.json() == {
        "email": "deadpool@example.com",
        "name": "Dead Pool",
        "id": response.json()['id'],
        "created_at": response.json()["created_at"]
    }
    
    
def test_get_all_users():
    response = client.get("/api/v1/User/get-all-users")
    assert response.status_code == 200
    assert any(d['email'] == 'deadpool@example.com' for d in response.json()) == True
    
    
def test_get_user_by_email():
    response = client.get("/api/v1/User/get-user-by-email/deadpool@example.com")
    assert response.status_code == 200
    assert response.json() == {
        "email": "deadpool@example.com",
        "password": response.json()["password"],
        "name": "Dead Pool",
        "id": response.json()['id'],
        "created_at": response.json()["created_at"]
    }
      
    
def test_delete_user():
    response = client.delete("/api/v1/User/delete/deadpool@example.com")
    assert response.status_code == 200
    assert response.json() == {
        "msg" : "User deletion successful"
        }