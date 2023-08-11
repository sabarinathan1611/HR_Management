from flask_login import login_required, current_user
from . import db
from .models import Employee,Attendance,Shift_time
from flask import Blueprint, render_template, request, flash, redirect, url_for,jsonify
import json
import datetime
from datetime import datetime

import os
views = Blueprint('views', __name__)


@views.route('/',methods=['POST','GET'])
@login_required
def admin():
    # employee =Employee.query.order_by(Employee.id)
    employee =Attendance.query.order_by(Attendance.date)   
    # sihft=Shift_time.query.order_by(Shift_time.id) 
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
    
        
@views.route('/delete-emp',methods=['POST'])
@login_required
def delete_employee():
    try:
        data = request.get_json()
        print(data)
        
        if not data or 'EmpId' not in data:
            return jsonify({'error': 'Invalid request data. EmpId is missing.'}), 400

        emp_id = data['EmpId']
        

        # Check if an employee with the given emp_id exists in the database
        employee = Employee.query.filter_by(id=int(emp_id)).first()
        
        attendance=Attendance.query.filter_by(id=int(emp_id)).all()
        for record in attendance:
            db.session.delete(record)

        if employee is None:
            return jsonify({'error': 'Employee not found.'}), 404

        # If the employee is found, delete the record from the database
        db.session.delete(employee)
        
        db.session.commit()

        return jsonify({'message': 'Employee deleted successfully.'}), 200

    except Exception as e:
        print(str(e))
        return jsonify({'error': str(e)}), 500

    return "Employee deleted successfully!", 200

   
    
    
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
      

        for attendance in attendance_records:
            print("SF: ",attendance.shift)
            shift = Shift_time.query.filter_by(id=1).first()
            print("SHIFT: ",shift)
            inTime = attendance.inTime
            print("IN TIME: ",inTime)
            shiftIntime = shift.shiftIntime
            print("SHIFT INTIME:",shiftIntime)
            shiftOuttime = shift.shift_Outtime

            # Calculate the lateBy time
            lateBy = calculate_time_difference(inTime, shiftIntime)
            attendance.lateBy = lateBy

            if attendance.outTime:
                outTime = attendance.outTime

                # Calculate the earlyGoingBy time
                earlyGoingBy = calculate_time_difference(outTime, shiftOuttime)
                print("EARLY GOING BY :",earlyGoingBy)
                if "-" in earlyGoingBy:
                   earlyGoingBy="00:00"
                attendance.earlyGoingBy = earlyGoingBy

                # Calculate the time duration between inTime and outTime
                time_worked = calculate_time_difference(inTime, outTime)
                print("Time Worked: ",time_worked)
                attendance.TotalDuration = time_worked

                # Calculate the overtime hours
                overtime_hours = calculate_time_difference(shiftOuttime, outTime)
                print("OVER TIME: ",overtime_hours)
                if "-" in  overtime_hours:
                    attendance.overtime = "00:00"
                else: 
                    attendance.overtime = overtime_hours
                    
               
            else:
                # If there's no outTime, consider the current time as the outTime
                out_time = datetime.now().strftime("%H:%M")
                earlyGoingBy = calculate_time_difference(out_time, shiftOuttime)
                attendance.earlyGoingBy = earlyGoingBy
                attendance.TotalDuration = calculate_time_difference(inTime, out_time)
                attendance.overtime = "00:00"

        # Commit the changes to the database for each employee
        db.session.commit()


@views.route('/adddd',methods=['POST','GET'])
def addd():
    
    calculate_Attendance()
    return redirect('/')
            

@views.route('/a2',methods=['POST','GET'])
def ad8d():
    # new_shift = Shift_time(shiftIntime="06:00",shift_Outtime="14:00",shiftType="8A",work_Duration="08:00")
    # db.session.add(new_shift)
    # db.session.commit()
    emp=Attendance.query.get(2)
    emp.inTime="08:16"
    emp.outTime="18:56"
    db.session.commit()
    

    return redirect('/')
