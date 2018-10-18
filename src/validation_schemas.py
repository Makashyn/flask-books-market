from marshmallow import Schema, fields



class BookSchema(Schema):
    name = fields.Str(required=True, error_messages={'required': 'Name of book is required'})
    description = fields.Str()
    price = fields.Float(
        required=True,
        error_messages={'required': 'Price of book is required'},
    )



