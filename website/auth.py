from flask import Blueprint, redirect, render_template, request, flash, url_for
from .models import User, Note
#from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_required, login_user, current_user, logout_user

auth = Blueprint('auth', __name__)
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user and user.password==password:
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

@auth.route('/delete-user/<int:id>', methods=['POST'])
#@login_required
def delete_user(id):
    user = User.query.get(id)
    if user:
        # Delete related records in the notes table
        Note.query.filter_by(user_id=user.id).delete()

        db.session.delete(user)
        try:
            db.session.commit()
        except Exception as e:
            print(e)
        flash('User deleted successfully', category='success')
    else:
        flash('User not found', category='error')
    print('user got deleted')    
    return redirect(url_for('views.home'))
