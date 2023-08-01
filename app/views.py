from flask_login import login_required, current_user
from . import db
from .models import Employee,Attendance
from flask import Blueprint, render_template, request, flash, redirect, url_for
import json
import datetime
from datetime import datetime

views = Blueprint('views', __name__)


@views.route('/',methods=['POST','GET'])
@login_required
def admin():
    # employee =Employee.query.order_by(Employee.id)
    employee =Attendance.query.order_by(Attendance.date)
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
    
@views.route('/profile-view')
@login_required
def profileView():
    try: 
        
        employee =Employee.query.order_by(Employee.id)
        
        
    except Exception as error:
        flash(error)
    current_date = datetime.now().date()
    return render_template('profile.html',employee=employee,current_date=current_date)



def update_wages_for_present_employees():
    
    current_date = datetime.datetime.now().date()

  
    employees = Employee.query.filter_by(workType='employee').all()

    for employee in employees:
        
        attendance_for_today = Attendance.query.filter_by(emp_id=employee.id, date=current_date).first()

        if attendance_for_today and attendance_for_today.attendance == 'present':
            # If the employee is present, increase the wages_per_Day by 1 for that day
            employee.wages_per_Day = str(int(employee.wages_per_Day) + 1)

   
    return db.session.commit()


def update_wages_for_present_daily_workers():
    
    current_date = datetime.datetime.now().date()

  
    employees = Employee.query.filter_by(workType='daily').all()

    for employee in employees:
        
        attendance_for_today = Attendance.query.filter_by(emp_id=employee.id, date=current_date).first()

        if attendance_for_today and attendance_for_today.attendance == 'present':
            # If the employee is present, increase the wages_per_Day by 1 for that day
            employee.wages_per_Day = str(int(employee.wages_per_Day) + 1)

   
    return db.session.commit()

def calculate_overtime():
    # Assuming Employee is your SQLAlchemy model for employees
    employees = Employee.query.all()

    for employee in employees:
        # Get all attendance records for the employee
        attendance_records = Attendance.query.filter_by(emp_id=employee.id).all()
        #to use the current date

        for attendance in attendance_records:
            in_time = datetime.strptime(attendance.inTime, '%H:%M:%S')
            
            if attendance.outTime:
                out_time = datetime.strptime(attendance.outTime, '%H:%M:%S')
            else:
                # If there's no outTime, consider the current time as the outTime
                out_time = datetime.now()
            
            # Calculate the time duration between inTime and outTime
            time_worked = out_time - in_time
            
            # Calculate the regular 8-hour work duration
            regular_work_hours = timedelta(hours=8)
            
            # Check if the time worked exceeds the regular work hours
            if time_worked > regular_work_hours:
                # Calculate the overtime hours
                overtime_hours = time_worked - regular_work_hours
                
                # Convert overtime_hours to a string in HH:MM format
                overtime_str = str(overtime_hours)
                
                # Update the overtime column in the Attendance table
                attendance.overtime = overtime_str

        # Commit the changes to the database for each employee
        db.session.commit()
