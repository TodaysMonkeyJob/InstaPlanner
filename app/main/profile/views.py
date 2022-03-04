# -*- coding:utf-8 -*-
from app import db
from app.models import Alcohol, Log, Comment, Permission, Tag, alcohol_tag
from flask import render_template, url_for, flash, redirect, request, abort
from flask_login import current_user
from .forms import SearchForm
from . import alcohol


@alcohol.route('/')
def index():
    search_word = request.args.get('search', None)
    search_form = SearchForm()
    page = request.args.get('page', 1, type=int)

    the_alcohols = Alcohol.query
    if not current_user.can(Permission.UPDATE_ALCOHOL_INFORMATION):
        the_alcohols = Alcohol.query.filter_by(hidden=0)


    pagination = the_alcohols.paginate(page, per_page=8)
    result_alcohols = pagination.items
    return render_template("profile.html", alcohols=result_alcohols, pagination=pagination, search_form=search_form,
                           title=u"List of alcohols")

