from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Email, Length, DataRequired


class SearchForm(FlaskForm):
    search = StringField(validators=[DataRequired()])
    submit = SubmitField(u"Search for")


class LoginForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(message=u"You forgot to fill in this item!"), Length(1, 64)])
    password = PasswordField(u'Password', validators=[DataRequired(message=u"You forgot to fill in this item!"),
                                                      Length(6, 32)])
    submit = SubmitField(u'Registered')

class PostForm(FlaskForm):
    file = StringField('File', validators=[DataRequired(message=u"You forgot to fill in this item!"), Length(1, 248)])
    description = StringField(u'Description', validators=[DataRequired])
    tag_people = StringField(u'Tags', validators=[DataRequired])
    submit = SubmitField(u'Registered')