from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Email, Length, DataRequired


class SearchForm(FlaskForm):
    search = StringField(validators=[DataRequired()])
    submit = SubmitField(u"Search for")


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(message=u"You forgot to fill in this item!"), Length(1, 64),
                                    Email(message=u"Is this your Email?")])
    password = PasswordField(u'Password',
                             validators=[DataRequired(message=u"You forgot to fill in this item!"),
                                         Length(6, 32)])
    submit = SubmitField(u'Registered')

