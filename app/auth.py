from flask_login import login_required, login_user, logout_user, current_user
from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash  
from .models import Login_HR,Employee

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

@auth.route('/hr-login',methods=['POST'])
def login_HR():
    if request.method == 'POST':
        email=request.form.get('email')
        password= request.form.get('password')
    
        dbemail = Login_HR.query.filter_by(email=email).first()
        if dbemail :
            if check_password_hash(dbemail.password, password):
                login_user(dbemail, remember=True)
                redirect(url_for('views.admin'))
                                
            else:
                flash("Incorrect Password",category='error')
        else:
            flash("Incorrect Email")
            
    return render_template('login.html')

            
    

                
                
                