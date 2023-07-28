from flask_login import login_required, login_user, logout_user, current_user
from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash  
from .models import Login_admin,Employee,Attendance
from . import db

def send_mail(email, body):
    sender_email = ""
    receiver_email = email
    password = ""
    message = body

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, message)
    print('*****Email sent!*****')
    server.quit()
    
    
auth = Blueprint('auth', __name__)

@auth.route('/admin-login',methods=['POST','GET'])
def login_admin():
    if request.method == 'POST':
        email=request.form.get('email')
        password= request.form.get('password')
    
        dbemail = Login_admin.query.filter_by(email=email).first()
        if dbemail :
            if check_password_hash(dbemail.password, password):
                login_user(dbemail, remember=True)
                redirect(url_for('views.admin'))
                                
            else:
                flash("Incorrect Password",category='error')
        else:
            flash("Incorrect Email")
            
    return render_template('login.html')

# @auth.route('/addUser')
            
    
@auth.route('/add',methods=['POST','GET'])
def addemp():
    if request.method == 'POST':
        empid=request.form.get('empid')
        print("empid: ",empid)
        
        name=request.form.get('name')
        print("Name: ",name)
        # attendance=request.form.get('attendance')
        dob=request.form.get('dob')
        print("dob",dob)
        
        # salary =request.form.get('salary')
        workType=request.form.get('workType')
        print("work Type: ")
        phoneNumber=request.form.get('phoneNumber')
        print("Phone")
        adharNumber=request.form.get('dob')
        wages_per_Day=request.form.get('wages_per_Day')
        gender=request.form.get('gender')
        # inTime=request.form.get('inTime')
        # outTime=request.form.get('outTime')
        address=request.form.get('address')
        
        
        
        
        
        addemp=Employee(id=empid,name=name,dob=dob,adharNumber=adharNumber,address=address,gender=gender)
        db.session.add(addemp)
        db.session.commit()
    return render_template('addemp.html')

                
                
                