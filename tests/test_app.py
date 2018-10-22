import pytest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import sys
sys.path.append('/home/makashyn/Documents/work/Book_market/src')

from view import book_list, create_book,  book_item, update_book_item, delete



def create_app(config_filename=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile(config_filename)
    db = SQLAlchemy(app)

    app.add_url_rule('/api/books', 'book_list', book_list, methods = ['GET'])
    app.add_url_rule('/api/books/create', 'create_book', create_book, methods=['POST'])
    app.add_url_rule('/api/books/<book_id>', 'book_item', book_item, methods=['GET'])
    app.add_url_rule('/api/books/<book_id>', 'update_book_item', update_book_item, methods=['PUT'])
    app.add_url_rule("/api/books/delete/<book_id>", 'delete', delete, methods = ['DELETE'])
    return app


@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app('flask_test.cfg')

    testing_client = flask_app.test_client()

    ctx = flask_app.app_context()
    ctx.push()

    yield testing_client

    ctx.pop()


def test_home_page(test_client):
    response = test_client.get('/api/books')
    assert response.status_code == 200

def test_books_filter(test_client):
    response = test_client.get('/api/books?=price_lt="2"')
    assert response.status_code == 200

def test_create_book(test_client):
    data = {
	    "name": "This is new post with test",
	    "price": 12,
	    "description": "sone"
    }
    response = test_client.post('/api/books/create',
                                json=data)
    assert response.status_code == 200

def test_book_item(test_client):
    response = test_client.get('/api/books/8')
    assert response.status_code == 200

def test_update_book_item(test_client):
    data = {
        "name": "this is updated name aasdasdwith tests",
        "price": 12,
        "description": "sone"
    }
    response = test_client.put('/api/books/9',
                                json=data)
    assert response.status_code == 200

def test_delete(test_client):
    response = test_client.delete('/api/books/delete/6')
    assert response.status_code == 200
