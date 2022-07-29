from pypos import create_app


def test_config():
    assert not create_app(
        {'FLASK_ENV': 'DEVELOPMENT'}).testing  # app.testing is false
    assert create_app({'TESTING': True}).testing


def test_hello(client):
    response = client.get('/hello')
    assert response.data == b'Hello, World!'
