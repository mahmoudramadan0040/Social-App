from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,DateField,TextAreaField
from wtforms.validators import DataRequired,length,Email,EqualTo
class PostFrom(FlaskForm):
    title = StringField(
        'title',
        validators=[
            DataRequired()
        ]
    )
    content = TextAreaField(
        'content',
        validators=[
            DataRequired()
        ]
    )
    date_posted =DateField(
        'date_posted'
    )
    submit = SubmitField(
        'Save Post'
    )