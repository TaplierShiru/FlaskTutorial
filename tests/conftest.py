import os
import tempfile

import pytest
from flaskr import create_app
from flaskr.db import get_db, init_db

with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf8')


@pytest.fixture
def app():
    # Create temporary file and return discription/path of it
    db_fd, db_path = tempfile.mkstemp()

    # Create test db/init app/fill test db
    app = create_app({
        'TESTING': True,        # App will be is test mode
        'DATABASE': db_path,
    })

    with app.app_context():
        init_db()
        get_db().executescript(_data_sql)

    yield app

    # Delete temp file
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    return app.test_client()    # Make requests w/o running the server


@pytest.fixture
def runner(app):
    return app.test_cli_runner()  # Creates a runner that cann call the click commands


class AuthActions:

    def __init__(self, client):
        self._client = client

    def login(self, username='test', password='test'):
        return self._client.post(
            '/auth/login',
            data={'username': username, 'password': password}
        )

    def logout(self):
        return self._client.get('/auth/logout')


@pytest.fixture
def auth(client):
    return AuthActions(client)

