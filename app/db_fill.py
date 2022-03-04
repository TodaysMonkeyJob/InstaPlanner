# -*- coding: utf-8 -*-

from app import app, db
from app.models import User, Role

app_ctx = app.app_context()
app_ctx.push()
db.create_all()
Role.insert_roles()

admin = User(name=u'root', email='root@gmail.com', password='password', major='administrator',
             headline=u"Temporary Administrator One", about_me=u"Graduated from the Department of Management, and likes to read, so I work as a librarian part-time.")
user1 = User(name=u'Ihor', email='akarin@Gmail.com', password='123456', major='Computer Science', headline=u"Student")
user2 = User(name=u'test', email='test@test.com', password='123456')
user3 = User(name=u'Dentist', email='xiaoming@163.com', password='123456')
user4 = User(name=u'User_user', email='lihua@yahoo.com', password='123456')


db.session.add_all(admin, user1, user2, user3, user4)
db.session.commit()

app_ctx.pop()
