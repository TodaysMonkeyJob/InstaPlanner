import json

from flask import render_template, url_for, flash, redirect, request

from app import db
from app.models import Profile
from . import profile
from .forms import LoginForm
from .forms import SearchForm
from app.get_profile_data import main


@profile.route('/', methods=['GET', 'POST'])
def index():
    search_form = SearchForm()
    page = request.args.get('page', 1, type=int)
    the_profiles = Profile.query
    pagination = the_profiles.paginate(page, per_page=8)
    result_profiles = pagination.items
    return render_template("profile_list.html", profiles=result_profiles, pagination=pagination,
                           search_form=search_form,
                           title=u"List of profiles")


@profile.route('/add_profile/', methods=['GET', 'POST'])
def add_profile():
    form = LoginForm()
    if form.validate_on_submit():
        the_profile = Profile(name=form.name.data, password=form.password.data)
        db.session.add(the_profile)
        db.session.commit()
        flash(u'Registered successfully!')
        return "<script>window.onload = window.close();</script>"
    return render_template("add_profile.html", form=form, title=u"Add new instagram profile")


@profile.route('/<name>')
def show_user(name):
    #main(profile.name, profile.password)
    with open(f'app/json_data/{name}.json', 'r') as file:
        profile_data = json.load(file)
        profile = Profile.query.filter_by(name=name).first_or_404()
        profile.post = profile_data["post"]
        profile.follower=profile_data["follower"]
        profile.following=profile_data["following"]
        profile.avatars = f"static/img/{name}.jpg"
        db.session.commit()
    profile = Profile.query.filter_by(name=name).first_or_404()
    return render_template('show_profile.html', profile=profile)
