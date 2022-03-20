import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
lm = LoginManager(app)
bootstrap = Bootstrap(app)

from app.main import main, auth, profile

for blueprint in [main, auth, profile]:
    app.register_blueprint(blueprint)

from app import models

exists_db = os.path.isfile(app.config['DATABASE'])
if not exists_db:
    from . import db_fill
