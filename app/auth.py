from flask_login import login_required, login_user, logout_user, current_user
from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from .models import Login_admin, Employee, Attendance, Shift_time,Backup,LoginEmp
from . import db
import datetime
from flask import current_app as app
from sqlalchemy.exc import SQLAlchemyError
import time
from datetime import datetime, timedelta
from .funcations import *





auth = Blueprint('auth', __name__)


@auth.route('/admin-login', methods=['POST', 'GET'])
def login():

    admin = Login_admin.query.filter_by(id=1).first()
    if admin:
        if request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')
            print("email",email)
            print("pwd :",password)

            dbemail = Login_admin.query.filter_by(email=email).first()
            if dbemail:
                if check_password_hash(dbemail.password, password):
                    login_user(dbemail, remember=True)
             
                    return redirect(url_for('views.admin'))

                else:
                    flash("Incorrect Password", category='error')
            else:
                flash("Incorrect Email", category='error')
    else:
        addAdmin = Login_admin(name="Admin", email="vsabarinathan1611@gmail.com", phoneNumber="123456789",
                               password="sha256$idRijyfQJjGQ3s7P$cedf4eb4aaaddab35c3423e31ab70bd5f60fb8b871f18e37ebec2359a818b6db")
        db.session.add(addAdmin)
        db.session.commit()
        print('Created Admin!')
   

    return render_template('login.html')


@auth.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/addemp', methods=['POST', 'GET'])
@login_required
def attendance():    
    try:

            file_path = os.path.join(app.config['EXCEL_FOLDER'], 'employee_data.xlsx')  # Use correct case 'EXCEL_FOLDER'
            addemployee(file_path)  # Call the data processing function
       

    except Exception as e:
        print("Error occurred:", e)
        db.session.rollback()  # Rollback in case of error
    return redirect(url_for('views.admin'))
