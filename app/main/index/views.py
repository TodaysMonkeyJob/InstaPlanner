from flask import render_template, request

from app.models import Permission
from . import main
from .forms import SearchForm

@main.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)


@main.route('/')
def index():
    search_form = SearchForm()
    page = request.args.get('page', 1, type=int)
    return render_template("index.html", search_form=search_form)
