
import pytest
from app import db, Book
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


def create_app(config_filename=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile(config_filename)
    db = SQLAlchemy(app)
    return app


@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app('flask_test.cfg')

    testing_client = flask_app.test_client()

    ctx = flask_app.app_context()
    ctx.push()

    yield testing_client

    ctx.pop()


@pytest.fixture(scope='module')
def init_database():

    db.create_all()

    book1 = Book(name="tests book", price=12.00)
    book2 = Book(name="tests book2", price=2.00)

    db.session.add(book1)
    db.session.add(book2)

    db.session.commit()
    yield db
    db.drop_all()

def test_home_page(test_client):
    response = test_client.get('')
    assert response.status_code == 200