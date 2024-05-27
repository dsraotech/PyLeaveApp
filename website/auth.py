from flask import Blueprint, redirect, render_template, request, flash, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_required, login_user, current_user, logout_user

auth = Blueprint('auth', __name__)
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            flash('User login successful', category='success')
            login_user(user, remember=True)
            return redirect(url_for('views.home'))
        else:
            flash('Invalid email or password', category='error')
    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        user_id = request.form.get('user_id')
        email = request.form.get('email')
        firstname = request.form.get('firstname')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if user_id:
            user = User.query.get(user_id)
            if user:
                user.email = email
                user.first_name = firstname
                if password1:
                    if password1 == password2:
                        user.password = generate_password_hash(password1, method='scrypt')
                    else:
                        flash('Confirmed password mismatch', category='error')
                        return redirect(url_for('auth.sign_up'))
                db.session.commit()
                flash('User updated successfully', category='success')
            else:
                flash('User not found', category='error')
        else:
            if User.query.filter_by(email=email).first():
                flash('Email ID already registered', category='error')
            elif len(email) < 4:
                flash('Email must be more than 4 characters', category='error')
            elif len(firstname) < 3:
                flash('First name must be more than 3 characters', category='error')
            elif len(password1) < 3:
                flash('Password length must be more than 3 characters', category='error')
            elif password1 != password2:
                flash('Confirmed password mismatch', category='error')
            else:
                newuser = User(email=email, first_name=firstname, password=generate_password_hash(password1, method='scrypt'))
                db.session.add(newuser)
                db.session.commit()
                flash('Signup successful', category='success')
                login_user(newuser, remember=True)
                return redirect(url_for('views.home'))

    users = User.query.all()
    return render_template("signup.html", user=current_user, users=users)

@auth.route('/delete-user/<int:id>', methods=['POST'])
@login_required
def delete_user(id):
    print('DSRAO deletion')
    user = User.query.get(id)
    if user:
        db.session.delete(user)
        db.session.commit()
        flash('User deleted successfully', category='success')
    else:
        flash('User not found', category='error')
    print('user got deleted')    
    return redirect(url_for('auth.sign_up'))
