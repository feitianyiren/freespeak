# This file contains form definitions for user submitted data

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()]) # the email function in this line is a WTForms mannerism, ensures the user inputs an email
    password = PasswordField('Password', validators=[DataRequired()])
    verify_password = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')]) # ensures the user typed their password correctly by making them enter it twice and verify with EqualTo()
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('This username is already taken.')
        
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if email is not None:
            raise ValidationError("This email is already in use.")

class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('About Me', validators=[Length(min=0, max=400)])
    submit = SubmitField('Submit')

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Please user a different name')

class PostForm(FlaskForm):
    post = TextAreaField('Speak your mind', validators=[
        DataRequired(), Length(min=1, max=4000)])
    submit = SubmitField('Submit')

