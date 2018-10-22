
import pytest

import sys
sys.path.append('../src')

from models import Book


@pytest.fixture(scope='module')
def new_book():
    book = Book(name="This is new book", description="This is discr", price=12.99)
    return book


def test_new_book(new_book):

    assert new_book.name == "This is new book"
    assert new_book.description == "This is discr"
    assert new_book.price == 12.99