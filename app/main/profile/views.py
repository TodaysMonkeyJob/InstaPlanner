# -*- coding:utf-8 -*-
from flask import render_template, request
from flask_login import current_user

from app.models import Profile, Permission
from . import profile
from .forms import SearchForm


@profile.route('/')
def index():
    search_form = SearchForm()
    page = request.args.get('page', 1, type=int)

    the_alcohols = Profile.query

    pagination = the_alcohols.paginate(page, per_page=8)
    result_alcohols = pagination.items
    return render_template("profile.html", alcohols=result_alcohols, pagination=pagination, search_form=search_form,
                           title=u"List of alcohols")


@profile.route('/add_profile/')
def add_profile():
    search_form = SearchForm()
    page = request.args.get('page', 1, type=int)

    the_alcohols = Profile.query

    pagination = the_alcohols.paginate(page, per_page=8)
    result_alcohols = pagination.items
    return render_template("add_profile.html", alcohols=result_alcohols, pagination=pagination, search_form=search_form,
                           title=u"Add new instagram profile")
