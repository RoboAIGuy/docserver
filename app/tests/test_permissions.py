import pytest

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

@pytest.fixture(scope="module", autouse=True)
def setup_and_teardown():
    setup_successful = False
    creator_user_data = {
            "email": "deadpoolwolverine@example.com",
            "password": "chimichangas4life",
            "name": "Dead Pool Wolverine"
        }
    reader_user_data = {
            "email": "flash@example.com",
            "password": "chipichipichapachapa",
            "name": "Flash"
        }
    document_data = {
            "title": "Test Document 3",
            "content": "This is a demo content",
            "creator": "deadpoolwolverine@example.com",
            "public": False
        }
    creator_response = ""
    creator_response = ""
    doc_response = ""
    
    try:
        # create creator user
        creator_response = client.post("/api/v1/User/create", json=creator_user_data)
        assert creator_response.status_code == 201
        
        # create reader user
        reader_response = client.post("/api/v1/User/create", json=reader_user_data)
        assert reader_response.status_code == 201
        
        # create test document
        doc_response = client.post("/api/v1/Document/create-document", json=document_data)
        assert doc_response.status_code == 201
        
        setup_successful = True
        yield
        
    # delete users and document if created
        if setup_successful:
            client.delete(f"/api/v1/User/delete/{creator_user_data['email']}")
            client.delete(f"/api/v1/User/delete/{reader_user_data['email']}")
            client.delete(f"/api/v1/Document/delete-document", json={"title": f"{document_data['title']}", "creator": f"{creator_user_data['email']}"})
        
    except Exception as e:
        print(f"An error occurred: {e}")
        print(creator_response.json())
        print(reader_response.json())
        print(doc_response.json())    
    
    
def test_read_document_by_title_and_user():
    response = client.get("/api/v1/Document/read-document/Test Document 3/flash@example.com")
    assert response.status_code == 403


def test_update_permission():
    response = ""
    try:
        response = client.put(
            "/api/v1/Permission/create-update-permission/deadpoolwolverine@example.com",
            json = {
                "document_title": "Test Document 3",
                "user_email": "flash@example.com",
                "can_read": True,
                "can_write": False,
                "can_delete": False
                },
            )
        assert response.status_code == 200
    except Exception as e:
        print(f"An error occurred: {response.json()}")
        assert False


def test_read_document_by_title_and_user_after_update():
    response = client.get("/api/v1/Document/read-document/Test Document 3/flash@example.com")
    assert response.status_code == 200
    assert response.json()["title"] == "Test Document 3"
    assert response.json()["content"] == "This is a demo content"