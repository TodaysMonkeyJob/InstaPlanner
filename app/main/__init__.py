# -*- coding:utf-8 -*-
from app import lm
from app.models import User


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


from .index import main
from .auth import auth
from .profile import alcohol
