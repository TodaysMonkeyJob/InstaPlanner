from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, FileField
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
    post_image = FileField("Photo", validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    description = TextAreaField(validators=[])
    tag_people = StringField(u'People', validators=[])
    tag_location = StringField(u'Location', validators=[])
    submit = SubmitField(u'Registered')