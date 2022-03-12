from app.models import Profile as model_Profile
from flask import url_for, jsonify
from flask_restful import Resource, marshal_with, abort
from . import api, parser, default_per_page
from .fields import profile_list


@api.route('/profile/')
class ProfileList(Resource):
    @marshal_with(profile_list)
    def get(self):
        args = parser.parse_args()
        page = args['page'] or 1
        per_page = args['per_page'] or default_per_page
        pagination = model_Profile.query.paginate(page=page, per_page=per_page)
        items = pagination.items
        prev = None
        if pagination.has_prev:
            prev = url_for('api.profilelist', page=page - 1, count=per_page, _external=True)
        next = None
        if pagination.has_next:
            next = url_for('api.profilelist', page=page + 1, count=per_page, _external=True)
        return jsonify({
            'items': items,
            'prev': prev,
            'next': next,
            'total': pagination.total,
            'pages_count': pagination.pages,
            'current_page': pagination.page,
            'per_page': per_page,
        })