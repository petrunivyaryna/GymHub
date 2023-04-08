import datetime
from flask_wtf import FlaskForm
from validate_email import validate_email as own_valid # for checking if the email is exist
# FileField: place for uploading a picture
# FileAllowed: what kind of files we want to allow to be uploded (in our case jpg, png, jpeg)
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user # getting the information about the current user
from wtforms import (StringField, PasswordField, SubmitField, BooleanField,
                    DateField, SelectField, TimeField) # for forms
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from flaskblog.models import User, Training # refering to database
from datetime import datetime, date


class RegistrationForm(FlaskForm):
    """
    This class is for registration form.
    """
    username = StringField("Ім'я користувача", validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Електронна адреса', validators = [DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    confirm_password = PasswordField('Підтвердити пароль',
                                    validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Зареєструватися')

    def validate_username(self, username): # to check if the username is already exist
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("Такий користувач вже існує. Будь ласка, виберіть інше ім'я користувача.")

    def validate_email(self, email): # to check if the email is already exist
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Така електронна пошта вже використовується. Будь ласка, виберіть іншу.')
        
        if not own_valid(email.data, verify=True):
            raise ValidationError("Неправильна адреса електронної пошти.")

class LoginForm(FlaskForm):
    """
    This class is for login form.
    """
    email = StringField('Електронна адреса', validators = [DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember = BooleanField("Запам'ятати мене")
    submit = SubmitField('Увійти')

class UpdateAccountForm(FlaskForm):
    """
    This class for updating the account information.
    """
    username = StringField("Ім'я користувача", validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Електронна адреса', validators = [DataRequired()])
    picture = FileField('Змінити фотографію', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Оновити')
    cancel = SubmitField('Скасувати')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError("Такий користувач вже існує. Будь ласка, виберіть інше ім'я користувача.")

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Така електронна пошта вже використовується. Будь ласка, виберіть іншу.')

            if not own_valid(email.data, verify=True):
                raise ValidationError("Неправильна адреса електронної пошти.")

class RequestResetForm(FlaskForm):
    """
    This class is for requesting the reset password.
    """
    email = StringField('Електронна адреса', validators=[DataRequired()])
    submit = SubmitField('Запит на скидання пароля')

    def validate_email(self, email):
        """
        This function has to check if there is the account with this email.
        """
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('Облікового запису з такою електронною поштою не існує. Вам необхідно спочатку зареєструватись.')

class ResetPasswordForm(FlaskForm):
    """
    This class is for reseting the password.
    """
    password = PasswordField('Пароль', validators=[DataRequired()])
    confirm_password = PasswordField('Підтвердити пароль',
                                    validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Запит на скидання пароля')

class ChooseTrainerForm(FlaskForm):
    """
    This form is for choosing the trainer and the date and time.
    """
    trainername = SelectField('Тренери', choices=[("Артем Скопа", "Артем Скопа"), ("Владислав Борисюк", "Владислав Борисюк"), ("Наталя Кравченко", "Наталя Кравченко"), ("Костянтин Новацький", "Костянтин Новацький")])
    entrydate = DateField('Дата', format='%Y-%m-%d', validators=[DataRequired()], render_kw={"class": "datepicker"})
    entrytime = TimeField('Час', format='%H:%M', validators=[DataRequired()])
    submit = SubmitField('Обрати')

    def validate_entrydate(self, entrydate):
        # checking if the training is already booked.
        my_entrytime = self.entrytime.data
        my_datatime = datetime.combine(entrydate.data, my_entrytime)
        trainer = self.trainername.data
        training = Training.query.filter_by(trainer=trainer, date=my_datatime).first()
        if training is not None:
            raise ValidationError('На жаль, цей тренер уже зайнятий у вибраний Вами час.')

        # setting up the bounderies in time.
        current_date = datetime.now()
        if entrydate.data.year != 2023:
            raise ValidationError('Запис доступний лише на 2023 рік.')
        else:
            if entrydate.data.month < current_date.month:
                raise ValidationError("На жаль, Ви не можете повернутися в минуле.")
            if entrydate.data.month == current_date.month:
                if entrydate.data.day < current_date.day:
                    raise ValidationError("На жаль, Ви не можете повернутися в минуле.")

        # check if the trainer is available in this date.
        date_object = entrydate.data
        day = date_object.weekday()
        trainername = self.trainername.data
        if trainername == 'Артем Скопа':
            if day not in [0, 2, 4]:
                raise ValidationError("На жаль, на цей день тижня відсутні тренування з цим тренером.")
        elif trainername == 'Владислав Борисюк':
            if day not in [1, 4]:
                raise ValidationError("На жаль, на цей день тижня відсутні тренування з цим тренером.")
        elif trainername == 'Костянтин Новацький':
            if day != 5:
                raise ValidationError("На жаль, на цей день тижня відсутні тренування з цим тренером.")
        elif trainername == 'Наталя Кравченко':
            if day not in [0, 2, 3]:
                raise ValidationError("На жаль, на цей день тижня відсутні тренування з цим тренером.")

    # check if the trainer is available in this time.
    def validate_entrytime(self, entrytime):
        time = datetime.combine(date.today(), entrytime.data)
        hour = time.hour
        minutes = time.minute
        trainername = self.trainername.data
        if trainername == 'Артем Скопа':
            if (hour != 18 and hour != 19) or minutes != 0:
                raise ValidationError("На жаль, на цю годину відсутні тренування з цим тренером.")
        elif trainername == 'Владислав Борисюк':
            if (hour != 17 and hour != 18) or minutes != 30:
                raise ValidationError("На жаль, на цю годину відсутні тренування з цим тренером.")
        elif trainername == 'Костянтин Новацький':
            if (hour != 10 and hour != 12) or minutes != 0:
                raise ValidationError("На жаль, на цю годину відсутні тренування з цим тренером.")
        elif trainername == 'Наталя Кравченко':
            if (hour != 17 and hour != 19 and hour != 20) or minutes != 0:
                raise ValidationError("На жаль, на цю годину відсутні тренування з цим тренером.")

