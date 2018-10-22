from app import app, db
from flask import request
from flask import jsonify, abort
import json
from models import Book

from validation_schemas import BookSchema
from marshmallow import ValidationError

from helper import filters, create_books_list



@app.route("/api/books", methods=['GET'])
def book_list():
    if request.args:
        list_data = filters(request.args, Model=Book)
        return jsonify(list_data)
    list_data = []
    queryset = Book.query.all()
    if queryset:
        list_data = create_books_list(queryset)[:]
    return jsonify(list_data)

@app.route("/api/books/create", methods=['POST'])
def create_book():

    data = request.json
    if data:
        schema = BookSchema()
        result_of_validation = schema.load(data)
        if result_of_validation.errors:
            for error in result_of_validation.errors.items():
                raise ValidationError(error[0][0] + " : " + error[1][0])

        new_post = Book(
            name=result_of_validation.data['name'],
            description=result_of_validation.data['description'],
            price=result_of_validation.data['price']
        )
        db.session.add(new_post)
        db.session.commit()
        return 'Success'
    else:
        abort(404)

@app.route("/api/books/<book_id>", methods=['GET'])
def book_item(book_id):
    queryset = Book.query.filter_by(id=book_id).first_or_404()
    return jsonify([{
        'id': queryset.id,
        'name': queryset.name,
        'description': queryset.description,
        'price': queryset.price
    }])



@app.route("/api/books/<book_id>", methods=['PUT'])
def update_book_item(book_id):
    queryset = Book.query.filter_by(id=book_id).first_or_404()
    data = request.json
    not_updated_obj = {
        'name': queryset.name,
        'description': queryset.description,
        'price': queryset.price
    }
    for update_element in data:
        not_updated_obj[update_element] = data[update_element]
    schema = BookSchema()
    result_of_validation = schema.load(not_updated_obj)
    if result_of_validation.errors:
        for error in result_of_validation.errors.items():
            raise ValidationError(error[0][0] + " : " + error[1][0])
    try:
        Book.query.filter_by(id=book_id).update(result_of_validation.data)
        db.session.commit()
        return 'Success'
    except:
        abort(404)

@app.route("/api/books/delete/<book_id>", methods=['DELETE'])
def delete(book_id):
    queryset = Book.query.filter_by(id=book_id).delete()
    db.session.commit()
    return "Success"