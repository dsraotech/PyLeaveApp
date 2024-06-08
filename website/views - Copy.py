#view.py
from flask import Blueprint, render_template, redirect, request, flash, jsonify, url_for
from flask_login import login_required, current_user
from .models import Note, User
from werkzeug.security import generate_password_hash, check_password_hash
import json
from . import db, engine
from flask_login import login_required, login_user, current_user, logout_user
from sqlalchemy.orm import Session
from sqlalchemy import text

views = Blueprint('views', __name__)
@views.route('/', methods=['GET'])
@login_required
def home():
    with engine.connect() as conn:
        mytext = "SELECT id_no,sno,to_char(fromdate,'DD-MON-YYYY') fromdate,to_char(todate,'DD-MON-YYYY') todate,descr leave_type, applieddays,reason FROM TLEAVES A, codes_master B"
        mytext = mytext+" WHERE b.group_code=16 AND a.leave_type=b.sub_code"
        select_query = text(mytext)
        result = conn.execute(select_query)   
    return render_template("home.html", user=current_user, Result=result)

@views.route("/delete-note", methods=['POST'])
def delete_note():
    note = json.loads(request.data)
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
    if request.method=='POST':
       fdate = request.form.get('leave_from_date')
    return render_template("leaveentry.html", user=current_user)



@views.route("/check-balance", methods=['POST','GET'])
def checkbalance():
    flash("not a valid resources")
    return jsonify({'message': "Not valid"})