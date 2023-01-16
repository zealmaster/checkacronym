from flask import Flask, request, render_template, session, url_for, Blueprint, flash, redirect
from .model import Users
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user

auth = Blueprint('auth', __name__, url_prefix='/')


# class NameForm(FlaskForm):
#     firstname = StringField('First Name',  validators=[InputRequired()])
#     lastname = StringField('Last Name', validators=[InputRequired()])
#     email = StringField('Email', validators=[InputRequired()])
#     password = PasswordField('Enter password', validators=[InputRequired()])
#     password1 = PasswordField('Confirm password', validators=[InputRequired()])
#     submit = SubmitField('Submit')
#     login = SubmitField('Login')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = Users.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Login Successfully', category='success')
                login_user(user, remember=True)
                return redirect(url_for('view.index'))
            else:
                flash('Incorrect password. Try again', category='warning')
        else:
            flash('Email does not exist.', category='warning')

    return render_template('login.html', boolean=True, user=current_user)


# Create route for sign up
@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        email = request.form.get('email')
        password = request.form.get('password')
        password1 = request.form.get('password1')
        password_hashed = generate_password_hash(password, method='sha256')
        user = Users.query.filter_by(email=email).first()
        if user:
            flash('Email already exist', category='warning')
            return redirect('/signup')
        elif password != password1:
            flash("Password does not match")
            return redirect('/signup')

        else:
            new_user = Users(firstname=firstname, lastname=lastname, email=email, password=password_hashed)
            db.session.add(new_user)
            db.session.commit()
            # login_user(user, remember=True)
            flash("Your account was created successfully", category='success')
            return redirect('/login')

    return render_template('signup.html', user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')

