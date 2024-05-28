#view.py
from flask import Blueprint, render_template, redirect, request, flash, jsonify, url_for
from flask_login import login_required, current_user
from .models import Note, User
from werkzeug.security import generate_password_hash, check_password_hash
import json
from . import db
from flask_login import login_required, login_user, current_user, logout_user
 
views = Blueprint('views', __name__)
@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')
        if len(note) < 1:
            flash('Please enter note data', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')
    return render_template("home.html", user=current_user)

@views.route("/delete-note", methods=['POST'])
def delete_note():
    print("start deleting the note")
    note = json.loads(request.data)
    print(note)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note and note.user_id == current_user.id:
        db.session.delete(note)
        db.session.commit()
        flash('Note deleted', category='success')
    return jsonify({})

@views.route("/approval", methods=['GET','POST'])
def leaveapproval():
    # user = User.query.get(current_user.id)
    # print("USER : ",type(user))
    # login_user(user, remember=True)
    return render_template("approval.html",user=current_user)

@views.route("/reports", methods=['GET','POST'])
def reports():
    return render_template("reports.html",user=current_user)

@views.route('/leaveentry', methods=['GET', 'POST'])
def leaveentry():
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
                        return redirect(url_for('views.home'))
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

