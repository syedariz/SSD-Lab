import pytest
from app import app, db, Ariza

@pytest.fixture
def client():
    # Setup: Configure app for testing with an in-memory database
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.drop_all()

def test_home_page(client):
    """Checks if the home page loads successfully."""
    response = client.get('/')
    assert response.status_code == 200

def test_add_entry(client):
    """Checks if a record can be added to the database."""
    response = client.post('/', data={
        'title': 'Jenkins Test',
        'content': 'Testing pytest integration'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Jenkins Test' in response.data

def test_delete_entry(client):
    """Checks if a record can be deleted."""
    with app.app_context():
        new_entry = Ariza(title="Delete Me", content="Temp content")
        db.session.add(new_entry)
        db.session.commit()
        entry_id = new_entry.id

    response = client.post(f'/delete/{entry_id}', follow_redirects=True)
    assert response.status_code == 200
    
    with app.app_context():
        assert db.session.get(Ariza, entry_id) is None