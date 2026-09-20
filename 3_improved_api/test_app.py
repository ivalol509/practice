import pytest
from app import app, db, Person, Note

@pytest.fixture
def client():
    app.config['TESTING'] = True

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    with app.test_client() as client:
        with app.app_context():
            db.drop_all()
            db.create_all()
            test_user = Person(name="aaa", email="aaa@gmail.com")
            db.session.add(test_user)
            db.session.commit()
        yield client

def test_check_empty(client):
    response = client.get('/notes')
    assert response.status_code == 200
    assert 'notes' in response.json
    assert 'page' in response.json
    assert 'per_page' in response.json
    
    assert response.json['notes'] == []
    assert response.json['count_of_notes'] == 0  
    assert response.json['page'] == 1

def test_create_note(client):
    new_note = {
        "user_id": 1,
        "title": "Hello",
        "text": "Kitty"
    }

    response = client.post('/notes', json=new_note)
    assert response.status_code == 201
    assert response.json['title'] == "Hello"

def test_update_note(client):
    old_note = {
        "user_id": 1,
        "title": "Hello",
        "text": "Kitty"
    }

    response1 = client.post('/notes', json=old_note)
    assert response1.status_code == 201

    update_note = {
        "title": "Bye-bye",
        "text": "Kitty"
    }

    response2 = client.put('/notes/1', json=update_note)
    assert response2.status_code == 200
    assert response2.json['title'] == "Bye-bye"

def test_delete_note(client):
    note = {
            "user_id": 1,
            "title": "Hello",
            "text": "Kitty"
        }
    client.post('/notes', json=note)
    response = client.delete('/notes/1')
    assert response.status_code == 204

def test_create_note_missing_fields(client):
    bad_note = {
        "user_id": 1,
        "title": "Без текста"
    }
    response = client.post('/notes', json=bad_note)
    assert response.status_code == 400
    assert "error" in response.json

# py -m pytest 3_improved_api/test_app.py 