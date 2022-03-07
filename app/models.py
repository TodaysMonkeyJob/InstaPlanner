# -*- coding: utf-8 -*-
import json
from datetime import datetime, timedelta

import bleach
from app import db, lm, avatars
from flask import current_app, url_for
from flask_login import UserMixin, AnonymousUserMixin
from markdown import markdown
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True)
    name = db.Column(db.String(64))
    password_hash = db.deferred(db.Column(db.String(128)))
    major = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    headline = db.Column(db.String(32), nullable=True)
    about_me = db.deferred(db.Column(db.Text, nullable=True))
    about_me_html = db.deferred(db.Column(db.Text, nullable=True))
    avatar = db.Column(db.String(128))
    member_since = db.Column(db.DateTime(), default=datetime.utcnow)

    @property
    def password(self):
        raise AttributeError('password is not readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email.lower() == current_app.config['FLASKY_ADMIN'].lower():
                self.role = Role.query.filter_by(permissions=0x1ff).first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()
        self.member_since = datetime.now()

    def can(self, permissions):
        return self.role is not None and \
               (self.role.permissions & permissions) == permissions

    def is_administrator(self):
        return self.can(Permission.ADMINISTER)



    def __repr__(self):
        return '<User %r>' % self.email


    def avatar_url(self, _external=False):
        if self.avatar:
            avatar_json = json.loads(self.avatar)
            if avatar_json['use_out_url']:
                return avatar_json['url']
            else:
                return url_for('_uploads.uploaded_file', setname=avatars.name, filename=avatar_json['url'],
                               _external=_external)
        else:
            return url_for('static', filename='img/avatar.png', _external=_external)

    @staticmethod
    def on_changed_about_me(target, value, oldvalue, initiaor):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquate', 'code', 'em', 'i',
                        'li', 'ol', 'pre', 'strong', 'ul', 'h1', 'h2', 'h3', 'p']
        target.about_me_html = bleach.linkify(
            bleach.clean(markdown(value, output_format='html'),
                         tags=allowed_tags, strip=True))


db.event.listen(User.about_me, 'set', User.on_changed_about_me)


class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False


lm.anonymous_user = AnonymousUser


class Permission(object):
    RETURN_PROFILE = 0x01
    BUY_PROFILE = 0x02
    WRITE_COMMENT = 0x04
    DELETE_OTHERS_COMMENT = 0x08
    UPDATE_OTHERS_INFORMATION = 0x10
    UPDATE_PROFILE_INFORMATION = 0x20
    ADD_PROFILE = 0x40
    DELETE_PROFILE = 0x80
    ADMINISTER = 0x100


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    @staticmethod
    def insert_roles():
        roles = {
            'User': (Permission.RETURN_PROFILE |
                     Permission.BUY_PROFILE |
                     Permission.WRITE_COMMENT, True),
            'Moderator': (Permission.RETURN_PROFILE |
                          Permission.BUY_PROFILE |
                          Permission.WRITE_COMMENT |
                          Permission.DELETE_OTHERS_COMMENT, False),
            'Administrator': (0x1ff, False)
        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
        db.session.commit()

    def __repr__(self):
        return '<Role %r>' % self.name


class Profile(db.Model):
    __tablename__ = 'profile'
    id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String(16), unique=True)
    title = db.Column(db.String(128))
    origin_title = db.Column(db.String(128))
    manufacturer = db.Column(db.String(128))
    distributor = db.Column(db.String(64))
    image = db.Column(db.String(512))
    price = db.Column(db.String(16))
    numbers = db.Column(db.Integer, default=10)
    summary = db.deferred(db.Column(db.Text, default=""))
    summary_html = db.deferred(db.Column(db.Text))
    catalog = db.deferred(db.Column(db.Text, default=""))
    catalog_html = db.deferred(db.Column(db.Text))
    hidden = db.Column(db.Boolean, default=0)



    @staticmethod
    def on_changed_summary(target, value, oldvalue, initiaor):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquate', 'code', 'em', 'i',
                        'li', 'ol', 'pre', 'strong', 'ul', 'h1', 'h2', 'h3', 'p']
        target.summary_html = bleach.linkify(
            bleach.clean(markdown(value, output_format='html'),
                         tags=allowed_tags, strip=True))

    @staticmethod
    def on_changed_catalog(target, value, oldvalue, initiaor):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquate', 'code', 'em', 'i',
                        'li', 'ol', 'pre', 'strong', 'ul', 'h1', 'h2', 'h3', 'p']
        target.catalog_html = bleach.linkify(
            bleach.clean(markdown(value, output_format='html'),
                         tags=allowed_tags, strip=True))

    def __repr__(self):
        return u'<Profile %r>' % self.title


db.event.listen(Profile.summary, 'set', Profile.on_changed_summary)
db.event.listen(Profile.catalog, 'set', Profile.on_changed_catalog)

