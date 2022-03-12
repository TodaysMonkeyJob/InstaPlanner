# -*- coding: utf-8 -*-

from app import app, db
from app.models import User, Role

app_ctx = app.app_context()
app_ctx.push()
db.create_all()
Role.insert_roles()
db.session.commit()

app_ctx.pop()
