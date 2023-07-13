from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,DateField,TextAreaField,ValidationError
from wtforms.validators import DataRequired,Length,Email,EqualTo
from flask_wtf.file import FileField, FileRequired
from flask_app.models import User
class PostFrom(FlaskForm):
    title = StringField(
        'title',
        validators=[
            DataRequired(),
            Length(min=5, max=50)
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
    privacy = StringField(
        'privacy',
        validators=[
            DataRequired()
        ]
    )
    submit = SubmitField(
        'Save Post'
    )


class Registration(FlaskForm):
    username = StringField(
        'username',
        validators = [
            DataRequired(),Length(min=5, max=50)
        ]
    )
    email = StringField(
        'email',
        validators=[
            DataRequired(),Email(),
            Length(max = 120)
        ]
    )

    password = PasswordField(
        'password',
        validators=[
            DataRequired()
        ]
    )

    confirm_password = PasswordField(
        'confirm password',
        validators=[
            DataRequired(), EqualTo("password")
        ]
    )

    photo = FileField(
        'photo',
        validators=[
            FileRequired()
        ]
    )
    submit = SubmitField(
        'Register'
    )
   
    def validate_email(self,email):
        email = User.query.filter_by(email = email.data).first()
        if email:
            raise ValidationError("This email already exists, Please choose another email")
        

    
class LoginForm(FlaskForm):
    email = StringField(
        'Username',
        validators=[
            DataRequired(),
            Email()
        ]
    )
    password = PasswordField(
        'Password',
        validators=[
            DataRequired()
        ]
    )
    submit = SubmitField(
        'Login'
    )

class EditUserForm(FlaskForm):
    username = StringField(
        'username',
        validators = [
            DataRequired(),Length(min=5, max=50)
        ]
    )

    photo = FileField(
        'photo',
        validators=[
            FileRequired()
        ]
    )

    submit = SubmitField(
        'save'
    )