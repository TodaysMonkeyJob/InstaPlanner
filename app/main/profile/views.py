from flask import render_template, url_for, flash, redirect, request

from app import db
from app.models import Profile
from . import profile
from .forms import LoginForm
from .forms import SearchForm


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
        the_profile = Profile(email=form.email.data, password=form.password.data)
        print(the_profile)
        db.session.add(the_profile)
        db.session.commit()
        flash(u'Registered successfully!')
        return redirect(request.args.get('next') or url_for('main.index'))
    return render_template("add_profile.html", form=form, title=u"Add new instagram profile")
