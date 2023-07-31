from flask_login import login_required, current_user
from . import db
from .models import Employee,Attendance
from flask import Blueprint, render_template, request, flash, redirect, url_for
import json

views = Blueprint('views', __name__)


@views.route('/',methods=['POST','GET'])
@login_required
def admin():
    # employee =Employee.query.order_by(Employee.id)
    employee =Employee.query.order_by(Employee.id)
    return render_template('admin.html',employee=employee)

@views.route('/edit',methods=['POST','GET'])
@login_required
def empEdit():
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
        dob_date = datetime.datetime.strptime(dob, '%Y-%m-%d').date()
        
        
        
        
        return redirect(url_for('views.admin'))
    
        
@views.route('/delete-emp')
@login_required
def deleteEmp():
    empJson=json.loads(request.data)
    empid=empJson['EmpId']
    employee= Employee.query.get(empid)
    attendances=employee.attendance
    
    for attendance in attendances:
        attendanceID=attendance.id
        empaddtendance=Attendance.query.get(attendanceID)
        db.session.delete(empaddtendance)
        db.commit()
    if employee.profile_pic == 'Default/Default.jpeg':

        return True
    
    else:
        path = app.config['UPLOAD_FOLDER'] + employee.profile_pic
        employee.profile_pic='Default/Default.jpeg'
        db.session.commit()
        os.remove(path)
        return redirect(url_for('views.admin'))
