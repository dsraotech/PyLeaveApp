#view.py
from flask import Blueprint, render_template, redirect, request, flash, jsonify, url_for
from flask_login import login_required, current_user
from .models import Note, User, Leavebal
from werkzeug.security import generate_password_hash, check_password_hash
import json
from . import db, engine
from flask_login import login_required, login_user, current_user, logout_user
from sqlalchemy.orm import Session
from sqlalchemy import text
from datetime import datetime
leavedata={}
views = Blueprint('views', __name__)
result={}
cl={}
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
   global result, cl
 #if request.method=='GET':
   with engine.connect() as conn:
    mytext = "select 99 code,'None' descr from dual  union all select SUB_CODE code,DESCR from codes_master where GROUP_CODE=16 "
    select_query = text(mytext)
    result = conn.execute(select_query)   
    cl = Leavebal.get_leave_balance(current_user.emp_code)
   if request.method=='POST':
      pass
      # Insert into the transactions
      # Update closing balance 
                 
   return render_template("leaveentry.html", user=current_user,leave_codes=result,cl_data=cl)



@views.route("/check-balance", methods=['POST'])
def checkbalance():
    formdata = request.form  # Access form data from request object
    cl = Leavebal.get_leave_balance(current_user.emp_code)
    fdate = request.form.get('leave_from_date')
    tdate = request.form.get('leave_to_date')
    #fdate = datetime.strptime(request.form.get('leave_from_date'),"%Y-%m-%d")
    #tdate = datetime.strptime(request.form.get('leave_to_date'),"%Y-%m-%d")
    ltype = (request.form.get('leave_type'))
    fdatetype = (request.form.get('leave_from_period'))  # Adjusted for consistency
    tdatetype = (request.form.get('leave_to_period'))  # Adjusted for consistency
    html_text=''
    if fdate==tdate and ((fdatetype=='1' and tdatetype=='0') or (fdatetype=='2' and tdatetype !='2')  or (fdatetype !='2' and tdatetype=='2') ) :
       html_text = html_text+'<tr><td>Date type Afternoon and Morning mismatch for same date</td></tr>'
    
    if ltype=='99':
       html_text = html_text+'<tr><td>Leave type should not be None</td></tr>'
       #flash("Leave type should not be None",category='error')
    if not fdate:
       html_text = html_text+'<tr><td>FROM date should not be blank</td></tr>'
       #flash("FROM date should not be blank",category='error')
    if not tdate:
       html_text = html_text+'<tr><td>TO date should not be blank</td></tr>'
       #flash("TO date should not be blank",category='error')
    if not fdatetype:
       html_text = html_text+'<tr><td>FROM date type should not be blank</td></tr>'
       #flash("FROM date type should not be blank",category='error')
    if not tdatetype:
       html_text = html_text+'<tr><td>TO date type should not be blank</td></tr>'
       #flash("FROM date type should not be blank",category='error')
        
    if fdate > tdate:
       html_text = html_text+'<tr><td>TO date always greater than FROM date</td></tr>'
       #flash("TO date always greater than FROM date",category='error')
    elif request.form.get('remarks')=="":
       html_text = html_text+'<tr><td>Remarks should not be blank</td></tr>'
       #flash("Remarks should not be blank",category='error')
    if (html_text) !='':
      html_text = '<table><tr><td>'+html_text+'</table>'
      return jsonify({'error': html_text})
    else:
       # calculating No of days eligible
       TotalDays = (datetime.strptime(tdate,"%Y-%m-%d")-datetime.strptime(fdate,"%Y-%m-%d")).days+1
       if fdatetype=='1':
          TotalDays=TotalDays-.5
       if tdatetype=='0':
          TotalDays=TotalDays-.5

      
       if ltype=='0' and TotalDays >cl.cl_bal:
          html_text = f'<table><tr><td>Insufficient CL balance {cl.cl_bal} against availing {TotalDays}</table>'
       if ltype=='1' and TotalDays >cl.el_bal:
          html_text = f'<table><tr><td>Insufficient AL balance {cl.el_bal} against availing {TotalDays}</table>'
       if ltype=='2' and TotalDays >cl.sl_bal:
          html_text = f'<table><tr><td>Insufficient SL balance {cl.sl_bal} against availing {TotalDays}</table>'
       if (ltype=='3' or ltype=='4') and TotalDays >cl.ot_bal:
          html_text = f'<table><tr><td>Insufficient OTHER balance {cl.ot_bal} against availing {TotalDays}</table>'


       if html_text !='':
          return jsonify({'error': html_text})
       else:           
          return jsonify({'message': 'SUCCESSFULLY Checked.  You may submit now'})

    #return render_template("leaveentry.html", user=current_user,leave_codes=result, htmltext=html_text)
