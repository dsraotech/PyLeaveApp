from flask import Blueprint, redirect, render_template, request, flash, url_for
from .models import User, Note
#from werkzeug.security import generate_password_hash, check_password_hash
from . import db, engine
from flask_login import login_required, login_user, current_user, logout_user
from sqlalchemy import text

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        empcode = request.form.get('userid')
        password = request.form.get('password')
        print(empcode, password)
        
        with engine.connect() as conn:
            mytext = f"SELECT emp_code, pw, generalname FROM invent.passwords@tams a, empprojtr_master@tams b WHERE a.emp_code=b.id_no AND emp_code = \'{empcode}\'"
            select_query = text(mytext)
            result = conn.execute(select_query).first()
        if result and result[1] == password:
            user = User(result[0],result[2])  # Create a User instance
            login_user(user, remember=True)
            flash('User login successful', category='success')
            return redirect(url_for('views.home'))
        else:
            flash('Invalid user code or password', category='error')
    
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
            pass
        flash('User deleted successfully', category='success')
    else:
        flash('User not found', category='error')

    return redirect(url_for('views.home'))
