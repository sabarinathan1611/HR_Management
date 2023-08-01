from flask_login import login_required, login_user, logout_user, current_user
from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash  
from .models import Login_admin,Employee,Attendance
from . import db
import datetime
import sched
import time
from datetime import datetime, timedelta

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
def login():
    try:
        admin = Login_admin.query.filter_by(id=1).first()
        if admin:
            if request.method == 'POST':
                email=request.form.get('email')
                password= request.form.get('password')
            
                dbemail = Login_admin.query.filter_by(email=email).first()
                if dbemail :
                    if check_password_hash(dbemail.password, password):
                        login_user(dbemail, remember=True)
                        redirect(url_for('views.admin'))
                        return redirect(url_for('views.admin'))
                                        
                    else:
                        flash("Incorrect Password",category='error')
                else:
                    flash("Incorrect Email")
        else:
            addAdmin=Login_admin(name="Admin",email="vsabarinathan1611@gmail.com",phoneNumber="123456789",password="sha256$idRijyfQJjGQ3s7P$cedf4eb4aaaddab35c3423e31ab70bd5f60fb8b871f18e37ebec2359a818b6db")
            db.session.add(addAdmin)
            db.session.commit()
            print('Created Admin!')
        flash("GIII",category='error')
    except Exception as error:
        flash(error,category='error')
    return render_template('login.html')

            
    
@auth.route('/add',methods=['POST','GET'])
@login_required
def addemp():
    if request.method == 'POST':
        
        empid=request.form.get('empid')
        name=request.form.get('name')
        dob=request.form.get('dob')
        workType=request.form.get('workType')
        phoneNumber=request.form.get('phoneNumber')
        adharNumber=request.form.get('adharNumber')
        wages_per_Day=request.form.get('wages_per_Day')
        gender=request.form.get('gender')
        address=request.form.get('address')
        email=request.form.get('email')
        
        print(dob)
        dob_date = datetime.strptime(dob, '%Y-%m-%d').date()
        
        employee=Employee.query.filter_by(id=empid).first()
        print(employee)
        if employee ==None:
            addemp=Employee(id=empid,email=email,name=name,dob=dob_date,adharNumber=adharNumber,address=address,gender=gender,phoneNumber=phoneNumber,workType=workType)
            db.session.add(addemp)
            db.session.commit()
            
        elif employee == True:
            print("Work")
            flash("User Alredy Iruku")
    return render_template('addemp.html')

                
@auth.route('/attendance',methods=['POST','GET'])
@login_required
def attendance():
    print(current_user)
    if current_user:
        if request.method =="POST":
            emp_id=request.form.get('empid')
            print(emp_id)
            wages_per_Day=request.form.get('wages')
            inTime=request.form.get('inTime')
            outTime=request.form.get('outTime')
            shift=request.form.get('shift')
            overtime=request.form.get('overTime')
            attendance=request.form.get('attendance')
            newattendance=Attendance(emp_id=emp_id,date=datetime.strptime('2023-08-02', '%Y-%m-%d').date(),wages_per_Day=wages_per_Day,inTime=inTime,outTime=outTime,shift=shift,overtime=overtime,attendance=attendance)
            db.session.add(newattendance)
            db.session.commit()
    else:
        return redirect(url_for('views.admin'))
        
    return render_template('attendance.html')