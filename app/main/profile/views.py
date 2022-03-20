from flask import render_template, flash, request, jsonify

from app import db
from app.models import Profile, Posts
from app.scenarious.scenario_selector import launch_scenario
from . import profile
from .forms import LoginForm
from .forms import SearchForm
from ...s3_help_functions import read_json_user_info_s3, read_posts_url, read_user_info_s3


@profile.route('/', methods=['GET', 'POST'])
def index():
    search_form = SearchForm()
    page = request.args.get('page', 1, type=int)
    the_profiles = Profile.query
    pagination = the_profiles.paginate(page, per_page=8)
    result_profiles = pagination.items
    for profile in result_profiles:
        profile_data = read_json_user_info_s3(profile.name)
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
    photo_id = list()
    posts_id = read_posts_url(name, f'{name}_post_id.txt')
    for post_id in posts_id:
        post_id = post_id.split('\n')[0]
        photo_id.append(post_id)
    profile = Profile.query.filter_by(name=name).first_or_404()
    return render_template('show_profile.html', profile=profile, photo_id=photo_id, search_form=search_form)

@profile.route('/<name>/user_info', methods=['GET'])
def update_user_info(name):
    profile = Profile.query.filter_by(name=name).first_or_404()
    try:
        launch_scenario(profile.name, profile.password, "get_user_data")
        profile_data = read_json_user_info_s3(profile.name)
        profile.post = profile_data["posts"]
        profile.follower = profile_data["followers"]
        profile.following = profile_data["following"]
        db.session.commit()
    except Exception as e:
        print(e)
    search_form = SearchForm()
    page = request.args.get('page', 1, type=int)
    the_profiles = Profile.query
    pagination = the_profiles.paginate(page, per_page=8)
    result_profiles = pagination.items
    return render_template("profile_list.html", profiles=result_profiles, pagination=pagination,
                           search_form=search_form,
                           title=u"List of info_data")

@profile.route('/<name>/user_posts_info', methods=['GET'])
def update_user_posts(name):
    try:
        profile = Profile.query.filter_by(name=name).first_or_404()
        launch_scenario(profile.name, profile.password, "save_user_photos")
    except Exception as e:
        print(e)

    search_form = SearchForm()
    photo_id = list()
    posts_id = read_posts_url(name, f'{name}_post_id.txt')
    for post_id in posts_id:
        post_id = post_id.split('\n')[0]
        photo_id.append(post_id)
    profile = Profile.query.filter_by(name=name).first_or_404()
    return render_template('show_profile.html', profile=profile, photo_id=photo_id, search_form=search_form)