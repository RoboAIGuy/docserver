import pytest
import requests

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

@pytest.fixture
def temporary_user():
    user_data = {
        "email": "deadpoolwolverine@example.com",
        "password": "chimichangas4life",
        "name": "Dead Pool Wolverine"
    }
    response = client.post("api/v1/User/create", json=user_data)
    assert response.status_code == 201
    yield user_data['email']
        
    client.delete(f"api/v1/User/delete/{user_data['email']}")


def test_create_document_not_public(temporary_user):
    response = client.post(
        "api/v1//Document/create-document",
        json={
            "title": "Test Document", 
            "content": "This is a test document",
            "creator": temporary_user,
            "public": False
            },
    )
    assert response.status_code == 201
    assert response.json()["title"] == "Test Document"
    assert response.json()["content"] == "This is a test document"
    
    
def test_get_all_documents():
    response = client.get("api/v1//Document/get-all-documents")
    assert response.status_code == 200
    assert any(d['title'] == 'Test Document' for d in response.json()) == True
    
    
def test_get_document_by_title():
    response = client.get("api/v1//Document/get-document-by-title/Test Document")
    assert response.status_code == 200
    assert response.json()["title"] == "Test Document"
    assert response.json()["content"] == "This is a test document"
    
    
def get_document_by_user(temporary_user):
    response = client.get(f"api/v1//Document/get-document-by-user/{temporary_user}")
    assert response.status_code == 200
    assert any(d['title'] == 'Test Document' for d in response.json()) == True
    
    
def test_read_document_by_title_and_user(temporary_user):
    response = client.get(f"api/v1/Document/read-document/Test Document/{temporary_user}")
    assert response.status_code == 200
    assert response.json()["title"] == "Test Document"
    assert response.json()["content"] == "This is a test document"
    assert response.json()["creator"] == temporary_user
    
    
def test_update_document(temporary_user):
    response = client.put(
        "api/v1/Document/update-document",
        json={
            "title": "Test Document",
            "content": "This is the updated test document",
            "creator": temporary_user,
            "public": True
            },
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Test Document"
    assert response.json()["content"] == "This is the updated test document"
    
    
def test_get_documents_classified_for_user(temporary_user):
    response = client.get(f"api/v1/Document/get-documents-classified-for-user/{temporary_user}")
    assert response.status_code == 200
    print(response.json()['created_documents'])
    assert any(d['title'] == 'Test Document' for d in response.json()['created_documents']) == True
    

def test_delete_document(temporary_user):
    response = client.delete(
        "api/v1/Document/delete-document",
        json={
            "title": "Test Document",
            "creator": temporary_user
            },
        )
    assert response.status_code == 200
    assert response.json() == {"msg" : "Document with title - 'Test Document' has been deleted"}