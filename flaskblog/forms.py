import datetime
from flask_wtf import FlaskForm
# FileField: place for uploading a picture
# FileAllowed: what kind of files we want to allow to be uploded (in our case jpg, png)
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user # getting the information about the current user
from wtforms import (StringField, PasswordField, SubmitField, BooleanField,
                    DateField, SelectField, TimeField) # for forms
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskblog.models import User # refering to database
from datetime import datetime, date


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators = [DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                    validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose another one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose another one.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators = [DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
    
class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators = [DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose another one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose another one.')
        
class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')
    def validate_email(self, email):
        """
        This function has to check if there is the account with this email.
        """
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                    validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Request Password Reset')

class ChooseTrainerForm(FlaskForm):
    trainername = SelectField('Trainers', choices=[("Артем Скопа", "Артем Скопа"), ("Владислав Борисюк", "Владислав Борисюк"), ("Костянтин Новацький", "Костянтин Новацький"), ("Наталя Кравченко", "Наталя Кравченко")])
    entrydate = DateField('Date', format='%Y-%m-%d', validators=[DataRequired()])
    entrytime = TimeField('Time', format='%H:%M', validators=[DataRequired()])
    submit = SubmitField('Choose trainer')

    def validate_entrydate(self, entrydate):
        current_date = datetime.now()
        if entrydate.data.year != 2023:
            raise ValidationError('You can only sign up for 2023!')
        else:
            if entrydate.data.month < current_date.month:
                raise ValidationError("You cannot sign up for a training that has already passed!")
            if entrydate.data.month == current_date.month:
                if entrydate.data.day < current_date.day:
                    raise ValidationError("You cannot sign up for a training that has already passed!")

    def validate_entrytime(self, entrytime):
        time = datetime.combine(date.today(), entrytime.data)
        hour = time.hour
        trainername = self.trainername.data
        if trainername == 'Артем Скопа':
            if hour != 18 and hour != 19:
                raise ValidationError("There are no available trainings for this hour!")
        elif trainername == 'Владислав Борисюк':
            if hour != 17 and hour != 18:
                raise ValidationError("There are no available trainings for this hour!")
        elif trainername == 'Костянтин Новацький':
            if hour != 10 and hour != 12:
                raise ValidationError("There are no available trainings for this hour!")
        elif trainername == 'Наталя Кравченко':
            if hour != 17 and hour != 19 and hour != 20:
                raise ValidationError("There are no available trainings for this hour!")
