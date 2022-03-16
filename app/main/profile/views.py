import json

from flask import render_template, url_for, flash, redirect, request

from app import db
from app.models import Profile, Posts
from . import profile
from .forms import LoginForm
from .forms import SearchForm
from app.scenarious.scenario_selector import launch_scenario

@profile.route('/', methods=['GET', 'POST'])
def index():
    search_form = SearchForm()
    page = request.args.get('page', 1, type=int)
    the_profiles = Profile.query
    pagination = the_profiles.paginate(page, per_page=8)
    result_profiles = pagination.items
    for profile in result_profiles:
        with open(f'app/info_data/{profile.name}.json', 'r') as file:
            profile_data = json.load(file)
            profile.post = profile_data["posts"]
            profile.follower = profile_data["followers"]
            profile.following = profile_data["following"]
            profile.avatars = f"static/img/{profile.name}.jpg"
            db.session.commit()
    return render_template("profile_list.html", profiles=result_profiles, pagination=pagination,
                           search_form=search_form,
                           title=u"List of info_data")


@profile.route('/add_profile/', methods=['GET', 'POST'])
def add_profile():
    form = LoginForm()
    if form.validate_on_submit():
        the_profile = Profile(name=form.name.data, password=form.password.data)
        try:
            launch_scenario(the_profile.name, the_profile.password, "get_user_data")
            db.session.add(the_profile)
            db.session.commit()
            flash(u'Registered successfully!')
            return "<script>window.onload = window.close();</script>"
        except Exception:
            return "<script>window.onload = window.close();</script>"
    return render_template("add_profile.html", form=form, title=u"Add new instagram profile")


@profile.route('/<name>/', methods=['GET'])
def show_profile(name):
    search_form = SearchForm()
    profile = Profile.query.filter_by(name=name).first_or_404()
    try:
        pass
        #launch_scenario(profile.name, profile.password, "save_user_photos")
        # with open(f'app/static/{name}/{name}_post_id.txt') as file:
        #     posts_id = file.readlines()
        #     for post_id in posts_id:
        #         post_id = post_id.split('\n')[0]
        #         the_post = Posts(name=name, post_id=post_id)
        #         db.session.add(the_post)
        #         db.session.commit()
    except Exception as e:
        print(e)
    post = Posts.query.filter_by(name=name)
    return render_template('show_profile.html', profile=profile, post=post, search_form=search_form)


