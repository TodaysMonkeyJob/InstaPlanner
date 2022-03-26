from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
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
    description = TextAreaField(validators=[DataRequired, Length(0, 2200)])
    tag_people = StringField(u'People', validators=[DataRequired])
    tag_location = StringField(u'Location', validators=[DataRequired])
    submit = SubmitField(u'Registered')