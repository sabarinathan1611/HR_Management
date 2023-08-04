from flask_login import login_required, current_user
from . import db
from .models import Employee,Attendance
from flask import Blueprint, render_template, request, flash, redirect, url_for
import json
import datetime
from datetime import datetime
from flask import current_app as app 

views = Blueprint('views', __name__)


@views.route('/',methods=['POST','GET'])
@login_required
def admin():
    # employee =Employee.query.order_by(Employee.id)
    employee =Attendance.query.order_by(Attendance.date)
    return render_template('admin.html',employee=employee)

@views.route('/edit', methods=['POST', 'GET'])
@login_required
def empEdit():
    if request.method == 'POST':
        empid = request.form.get('empid')
        name = request.form.get('name')
        dob = request.form.get('dob')
        workType = request.form.get('workType')
        phoneNumber = request.form.get('phoneNumber')
        adharNumber = request.form.get('adharNumber')
        wages_per_Day = request.form.get('wages_per_Day')
        gender = request.form.get('gender')
        address = request.form.get('address')
        dob_date = datetime.strptime(dob, '%Y-%m-%d').date()

        # Query the database for an employee with the given 'empid'
        emp = Employee.query.filter_by(id=empid).first()

        if emp:
            # Update the employee's data with the new information
            emp.name = name
            emp.dob = dob_date
            emp.workType = workType
            emp.phoneNumber = phoneNumber
            emp.adharNumber = adharNumber
            emp.wages_per_Day = wages_per_Day
            emp.gender = gender
            emp.address = address

            # Commit the changes to the database
            db.session.commit()
        else:
            flash('Employee not found!', 'error')

        # Redirect the user to the 'admin' page or route.
    return redirect(url_for('views.admin'))
    
        
@views.route('/delete-emp')
@login_required
def deleteEmp():
    try:
        empJson = request.get_json()  # Use 'get_json()' method to get JSON data from request
        empid = empJson['EmpId']
        
        # Retrieve the employee with the given 'EmpId'
        employee = Employee.query.get(empid)
        if employee is None:
            return "Employee not found!", 404
        
        # Delete associated attendance records
        attendances = employee.attendance
        for attendance in attendances:
            db.session.delete(attendance)
        
        # Check if the employee has a custom profile picture
        if employee.profile_pic != 'Default/Default.jpeg':
            path = os.path.join(app.config['UPLOAD_FOLDER'], employee.profile_pic)
            employee.profile_pic = 'Default/Default.jpeg'
            os.remove(path)
        
        # Commit changes to the database
        db.session.delete(employee)
        db.session.commit()

        return "Employee deleted successfully!", 200

    except Exception as e:
        # Handle any unexpected errors
        return str(e), 500
    
@views.route('/profile-view')
@login_required
def profileView():
    try: 
        
        employee =Employee.query.order_by(Employee.id)
        
        
    except Exception as error:
        flash(error)
    current_date = datetime.now().date()
    return render_template('profile.html',employee=employee,current_date=current_date)

def calculate_time_difference(time1_str, time2_str):
    # Convert time strings to datetime objects
    time1 = datetime.strptime(time1_str, '%H:%M')
    time2 = datetime.strptime(time2_str, '%H:%M')

    # Calculate the time difference
    time_difference = time2 - time1

    # Calculate the total minutes in the time difference
    total_minutes = time_difference.total_seconds() // 60

    # Calculate hours and remaining minutes
    hours = total_minutes // 60
    minutes = total_minutes % 60

    # Format the time difference as H:MM
    formatted_difference = f"{int(hours)}:{int(minutes):02d}"
    return formatted_difference

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

def calculate_Attendance():
    # Assuming Employee is your SQLAlchemy model for employees
    employees = Employee.query.all()

    for employee in employees:
        # Get all attendance records for the employee
        attendance_records = Attendance.query.filter_by(emp_id=employee.id).all()
        shift=Shift_time.query.filter_by(shiftType=employee.shift).first()
        #to use the current date

        for attendance in attendance_records:
            inTime=attendance.inTime
            outTime=attendance.outTime
            shiftIntime=shift.shiftIntime
            shiftOuttime=shift.shift_Outtime

            lateBy=calculate_time_difference(inTime,shiftIntime)
            
            if attendance.outTime:
                earlyGoingBy=calculate_time_difference(outTime,shiftOuttime)
                # Calculate the time duration between inTime and outTime
                time_worked = calculate_time_difference(inTime,outTime)
                
                
                # Calculate the regular 8-hour work duration
                regular_work_hours = shift.work_Duration
                overtime_hours = calculate_time_difference(shiftOuttime,outTime)
                attendance.overtime = overtime_hours

            else:
                # If there's no outTime, consider the current time as the outTime
                out_time = datetime.now()
            


        # Commit the changes to the database for each employee
        db.session.commit()


            
            
            