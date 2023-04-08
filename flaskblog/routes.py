import os # for making sure we save the photo in the same extension it was uploaded
import secrets # for generating random hex
import datetime
# to resize the image to 125 pixels in order to save a lot of space in our file system and speed up our web
from PIL import Image
from flask import render_template, url_for, flash, redirect, request # for redirecting to pagees, flashing messages, 
# running the html templates and for the request
from flaskblog import app, db, bcrypt, mail # to work with the database and mail
# forms that get from the forms.py and can use wen on site if field to be filled
from flaskblog.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                            RequestResetForm, ResetPasswordForm, ChooseTrainerForm)
# User to get the user from the database, Training to get the training from the database
from flaskblog.models import User, Training
from flask_login import login_user, current_user, logout_user, login_required # to work with the registration and login
from flask_mail import Message # to send the email to the user

@app.route("/")
@app.route("/main", methods=['GET', 'POST'])
def main():
    return render_template('main.html')

@app.route("/home", methods=['GET', 'POST'])
def home():
    form=RegistrationForm()
    return render_template('home.html', title='Про нас', form=form)

@app.route("/home_1", methods=['GET', 'POST'])
def home_1():
    form=RegistrationForm()
    return render_template('home_1.html', title='Про нас', form=form)

@app.route("/register", methods=['GET', 'POST'])
def register():
    # if the user is already logged in, we don't want to let him register again
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Ваш обліковий запис було створено! Тепер Ви можете увійти в систему.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    # if current_user.is_authenticated:
    #     return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        # bcrypt checks whether the decoding password which everytime generated differently
        # equals to the password that the user has entered
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            # checking if next parameter exists (next=%2Faccount), args is a dictionary
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Не вдалося увійти. Будь ласка, перевірте електронну адресу та пароль.', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main'))


def save_picture(form_picture):
    """
    function for saving the profile picture.
    """
    # for generating the random names for picture files
    random_hex = secrets.token_hex(8)
    # returns file name without the extension and then with the extention
    # _ unused variable
    _, f_ext = os.path.splitext(form_picture.filename)
    # for making sure we save the photo in the same extension it was uploaded
    picture_fn = random_hex + f_ext
    # creating one long path:
    # join the root path of picture with our picture directory path and then with picture filename
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    # correcting the size of the picture
    output_size = (250, 250)
    with Image.open(form_picture) as img:
        # Getting the size of the picture
        width, height = img.size
        # Finding the max size between wigth and height
        max_size = max(width, height)
        # Creating a new photo with white background
        padded_img = Image.new('RGB', (max_size, max_size), (155, 82, 27))
        # Place the input image in the center
        padded_img.paste(img, ((max_size - width) // 2, (max_size - height) // 2))
        # Reducing the size of the image
        padded_img.thumbnail(output_size)
        # Saving the image
        padded_img.save(picture_path)

    return picture_fn


@app.route("/account", methods=['GET', 'POST'])
@login_required # only for logged in ones
def account():
    """
    In this function we will update the account.
    Also it is for the user to see his trainings and to cancel them.
    """
    form = UpdateAccountForm()
    trainings = Training.query.filter_by(user_id = current_user.id)
    if form.validate_on_submit():
        # to update the picture
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        return redirect(url_for('account'))

    # to delete training if the user pressed the button 'cancel'
    elif request.method == 'POST' and 'cancel' in request.form:
        training_id = request.form.get('training_id')
        if training_id:
            training = Training.query.get(training_id)
            db.session.delete(training)
            db.session.commit()
            return redirect(url_for('account'))
    elif request.method == 'GET': # form already contains the previous information
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, trainings=trainings, form=form)


def send_reset_email(user):
    """
    This function has to send emails.
    """
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='noreply@demo.com', recipients=[user.email])
    msg.body = f"""To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}

If you did not make this request then simply ignore this email and no changes will be made.
"""
    mail.send(msg)

@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    """
    Checking if the user with this email has the account.
    """
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        # sending email only if the user exists
        # it uses the function above
        send_reset_email(user)
        flash('На Вашу електронну адресу було надіслано листа з інструкціями щодо скидання пароля.', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title='Reset Password', form=form)

@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token) # checking if the token is valid
    if user is None:
        flash('Це недійсний або застарілий токен.', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Ваш пароль було оновлено! Ви можете увійти в систему.', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title='Змінити пароль', form=form)

@app.route("/trainer", methods=['GET', 'POST'])
@login_required
def trainer():
    """
    This function add the training to the database.
    If the user's chosen trainer is available in chosen date and time
    then the user will be signed up for the training
    """
    form = ChooseTrainerForm()
    if form.validate_on_submit():
        my_datatime = datetime.datetime.combine(form.entrydate.data, form.entrytime.data)
        training = Training(trainer=form.trainername.data, date=my_datatime, author=current_user)
        db.session.add(training)
        db.session.commit()
        return redirect(url_for('account'))
    return render_template('trainer.html', title='Choose Trainer', form=form)

@app.route("/abonement")
@login_required
def abonement():
    form = RegistrationForm()
    return render_template('abonement.html', form=form)
