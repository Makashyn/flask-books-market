from app import app, db
from flask import request
from flask import jsonify, abort

from models import Book

from validation_schemas import BookSchema
from marshmallow import ValidationError

def create_books_list(queryset):
    list_data = []
    for item in queryset:
        list_data.append({
            'id': item.id,
            'name': item.name,
            'description': item.description,
            'price': item.price
        })
    return list_data


@app.route("/api/books", methods=['GET'])
def book_list():
    if request.args:
        list_data = []

        for filter_keyword in request.args:
            filter_condition = ''
            if '__' in filter_keyword:
                filter_condition = filter_keyword.split('__')[1]
            else:
                filter_condition = filter_keyword

            queryset = []

            if filter_condition == 'book':
                queryset = Book.query.filter(Book.name.contains(request.args.get(filter_keyword))).all()
            elif filter_condition == 'startswith':
                queryset = Book.query.filter(Book.name.startswith(request.args.get(filter_keyword)[1])).all()
            elif filter_condition == 'price_lt':
                queryset = Book.query.filter(Book.price < request.args.get(filter_keyword)).all()
            elif filter_condition == 'price_gt':
                queryset = Book.query.filter(Book.price > request.args.get(filter_keyword)).all()

            if queryset:
                list_data = create_books_list(queryset)[:]

        return jsonify(list_data)
    list_data = []
    queryset = Book.query.all()
    if queryset:
        list_data = create_books_list(queryset)[:]

    return jsonify(list_data)

@app.route("/api/create", methods=['POST'])
def create_book():
    if request.method == 'POST':
        try:
            data = request.json()
        except:
            abort(404)
        schema = BookSchema()
        result_of_validation = schema.load(data)
        if result_of_validation.errors:
            for error in result_of_validation.errors.items():
                raise ValidationError(error[0][0] + " : " + error[1][0])

        new_post = Book(name=data['name'], description=data['description'], price=data['price'])
        db.session.add(new_post)
        db.session.commit()


@app.route("/api/update/<book_id>", methods=['POST', 'GET'])
def update(book_id):
    queryset = Book.query.filter_by(id=book_id).first_or_404()
    if request.method == 'GET':
        if queryset:
            return jsonify([{
                'id': queryset.id,
                'name': queryset.name,
                'description': queryset.description,
                'price': queryset.price
            }])
    if request.method == 'POST':
         data = request.json()
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
            Book.query.filter_by(id=book_id).update(data)
            db.session.commit()
         except:
             abort(404)
         return "some"

@app.route("/api/delete/<book_id>", methods=['GET'])
def delete(book_id):
    queryset = Book.query.filter_by(id=book_id).delete()
    db.session.commit()
    abort(201)
