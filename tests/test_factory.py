from flaskr import create_app


def test_config():
    assert not create_app().testing, 'app not in test mode'
    assert create_app({'TESTING': True}).testing, 'init app not in test mode'


def test_hello(client):
    response = client.get('/hello')
    assert response.data == b'Hello, World!'

