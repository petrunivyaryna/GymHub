import datetime
from flask_wtf import FlaskForm
from validate_email import validate_email as own_valid
# FileField: place for uploading a picture
# FileAllowed: what kind of files we want to allow to be uploded (in our case jpg, png)
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user # getting the information about the current user
from wtforms import (StringField, PasswordField, SubmitField, BooleanField,
                    DateField, SelectField, TimeField) # for forms
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskblog.models import User, Training # refering to database
from datetime import datetime, date


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators = [DataRequired()])
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
        
        if not own_valid(email.data, verify=True):
            raise ValidationError("Invalid email address")

class LoginForm(FlaskForm):
    email = StringField('Email', validators = [DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators = [DataRequired()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Update')
    cancel = SubmitField('Cancel')

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

            if not own_valid(email.data, verify=True):
                raise ValidationError("Invalid email address")

class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
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
        # checking if the training is already booked.
        my_entrytime = self.entrytime.data
        my_datatime = datetime.combine(entrydate.data, my_entrytime)
        trainer = self.trainername.data
        training = Training.query.filter_by(trainer=trainer, date=my_datatime).first()
        if training is not None:
            raise ValidationError('The training has already been booked.')

        # setting uo the bounderies in time.
        current_date = datetime.now()
        if entrydate.data.year != 2023:
            raise ValidationError('You can only sign up for 2023!')
        else:
            if entrydate.data.month < current_date.month:
                raise ValidationError("You cannot sign up for a training that has already passed!")
            if entrydate.data.month == current_date.month:
                if entrydate.data.day < current_date.day:
                    raise ValidationError("You cannot sign up for a training that has already passed!")

        # check if the trainer is available in this date.
        date_object = entrydate.data
        day = date_object.weekday()
        trainername = self.trainername.data
        if trainername == 'Артем Скопа':
            if day not in [0, 2, 4]:
                raise ValidationError("There are no available trainings for this day of the week!")
        elif trainername == 'Владислав Борисюк':
            if day not in [1, 4]:
                raise ValidationError("There are no available trainings for this day of the week!")
        elif trainername == 'Костянтин Новацький':
            if day != 5:
                raise ValidationError("There are no available trainings for this day of the week!")
        elif trainername == 'Наталя Кравченко':
            if day not in [0, 2, 3]:
                raise ValidationError("There are no available trainings for this day of the week!")

    def validate_entrytime(self, entrytime):
        time = datetime.combine(date.today(), entrytime.data)
        hour = time.hour
        minutes = time.minute
        trainername = self.trainername.data
        if trainername == 'Артем Скопа':
            if (hour != 18 and hour != 19) or minutes != 0:
                raise ValidationError("There are no available trainings for this hour!")
        elif trainername == 'Владислав Борисюк':
            if (hour != 17 and hour != 18) or minutes != 30:
                raise ValidationError("There are no available trainings for this hour!")
        elif trainername == 'Костянтин Новацький':
            if (hour != 10 and hour != 12) or minutes != 0:
                raise ValidationError("There are no available trainings for this hour!")
        elif trainername == 'Наталя Кравченко':
            if (hour != 17 and hour != 19 and hour != 20) or minutes != 0:
                raise ValidationError("There are no available trainings for this hour!")


class GroupTrainings(FlaskForm):
    """
    This class should create the base of the page where the client can choose
    the group training.
    """
    book = SubmitField('Book')