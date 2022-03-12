from flask import url_for
from flask_restful import fields
from . import default_per_page

profile_fields = {
    'id': fields.Integer,
    'email': fields.String,
    'password': fields.String,
    # 'name': fields.String,
}
profile_list = {
    'items': fields.List(fields.Nested(profile_fields)),
    'next': fields.String,
    'prev': fields.String,
    'total': fields.Integer,
    'pages_count': fields.Integer,
    'current_page': fields.Integer,
    'per_page': fields.Integer,
}