from flask_login import login_required, current_user
from . import db
from .models import Employee,Attendance,Shift_time,Backup, late, leave,notification,NewShift
from flask import Blueprint, render_template, request, flash, redirect, url_for,jsonify
import json
import datetime
from flask import session
import pandas as pd
from flask import current_app as app
from datetime import datetime, timedelta
import os
from .funcations import *
from .sms import send_sms
from werkzeug.utils import secure_filename

import csv
from sqlalchemy import desc

views = Blueprint('views', __name__)
ALLOWED_EXTENSIONS = {'csv'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
from flask_socketio import emit
from app import socketio
@views.route('/',methods=['POST','GET'])
@login_required
def admin():
    try:
        inshift = Shift_time.query.filter_by(id=1).first()
        if not inshift:
            file_path = os.path.join(app.config['EXCEL_FOLDER'], '01-08-23.xls')  # Use correct case 'EXCEL_FOLDER'
            process_excel_data(file_path)  # Call the data processing function
        else:
            print("Shift not found")

    except Exception as e:
        print("Error occurred:", e)
        db.session.rollback()  # Rollback in case of error

    
    # employee =Employee.query.order_by(Employee.id)
    employee =Attendance.query.order_by(Attendance.id)   
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


@views.route('/calculate',methods=['POST','GET'])
def calculate():
    
    calculate_Attendance()
    # lol=Shift_time.query.filter_by(id=5).first()
    # lol.shiftIntime="14:00"
    # lol.shift_Outtime="22:00"
    # db.session.commit()
    # print(lol.shift_Outtime)
    
    return redirect('/')
            
# @views.route('/getshift',methods=['POST','GET'])
# def get_shift():
#     try:
#         inshift = Shift_time.query.filter_by(id=1).first()
#         if not inshift:
#             file_path = os.path.join(app.config['Excel_FOLDER'], '01-08-23.xls')
#             process_excel_data(file_path)  # Call the data processing function
#         else:
#             print("Shift not found")

#     except Exception as e:
#         print("Error occurred:", e)
#         db.session.rollback()  # Rollback in case of error
    
#     return redirect(url_for('views.viewShift'))  # Redirect to viewShift after processing
    
 # new_shift = Shift_time(shiftIntime="06:00",shift_Outtime="14:00",shiftType="8A",work_Duration="08:00")
    # db.session.add(new_shift)
    # db.session.commit()
    # emp=Attendance.query.get(2)
    # emp.inTime="08:16"
    # emp.outTime="18:56"
    # db.session.commit()
@views.route('/shift')
def viewShift():
    
    records=Shift_time.query.order_by(Shift_time.id)  
    return render_template('shift.html',records=records)

@views.route('/attendance')
def readXl_update_atten():
    try:
            file_path = os.path.join(app.config['EXCEL_FOLDER'], 'attendance.xlsx')  # Use correct case 'EXCEL_FOLDER'
            attend_excel_data(file_path)  # Call the data processing function
       

    except Exception as e:
        print("Error occurred:", e)
        db.session.rollback()  # Rollback in case of error    
    return redirect(url_for('views.calculate'))

@views.route('/backup', methods=['POST', 'GET'])
def backup_data():
            

    # Retrieve all records from the Attendance table
    attendance_records = Attendance.query.all()

    # Create new Backup objects and copy data from Attendance records
    backup_records = []
    for attendance_record in attendance_records:
        backup_record = Backup(
            date=attendance_record.date,
            emp_id=attendance_record.emp_id,
            attendance=attendance_record.attendance,
            wages_per_Day=attendance_record.wages_per_Day,
            inTime=attendance_record.inTime,
            outTime=attendance_record.outTime,
            overtime=attendance_record.overtime,
            shiftType=attendance_record.shiftType,
            shiftIntime=attendance_record.shiftIntime,
            shift_Outtime=attendance_record.shift_Outtime,
            TotalDuration=attendance_record.TotalDuration,
            lateBy=attendance_record.lateBy,
            earlyGoingBy=attendance_record.earlyGoingBy,
            punchRecords=attendance_record.punchRecords
        )
        backup_records.append(backup_record)

    # Add the new Backup records to the database
    db.session.bulk_save_objects(backup_records)

    # Delete the records from the Attendance table
    for attendance_record in attendance_records:
        db.session.delete(attendance_record)

    # Commit the changes to the database
    db.session.commit()
    return redirect(url_for('views.admin'))


@views.route('/dashboard',methods=['POST','GET'])
def dashboard():
    return render_template('dashboard.html')


#mahaveer
# Your route handlers and SocketIO events go here
# @views.route('/')
# def index():
#     return render_template('index.html')


@views.route('/late_form_page')
def late_form_page():
    return render_template('emp_late.html')


@views.route('/leave_form_page')
def leave_form_page():
    return render_template('emp_leave.html')


@socketio.on('connect')
def handle_connect():
    print('Client Connected')


@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')    

@views.route('/late_approve',methods=['POST','GET'])
def late_approve():
    user = json.loads(request.data)
    userID = user['userId']
    user = late.query.filter_by(emp_id=userID).first()
    print(" USER : ",user)
    current_user='hr'
    if current_user=='hr':
        user.hr_approval='Approved'
        user.status='Approved'
        db.session.commit()
        print("Hr Approval ", user.hr_approval)
        print("Status ", user.status)
        emit('late_hr_approval_update', {'userId': userID, 'hr_approval': user.hr_approval}, broadcast=True)

@views.route('/leave_approve',methods=['POST','GET'])
def leave_approve():
    user = json.loads(request.data)
    userID = user['userId']
    user = leave.query.filter_by(emp_id=userID).first()
    print(" USER : ",user)
    current_user='hr'
    if current_user=='hr':
        user.hr_approval='Approved'
        user.status='Approved'
        db.session.commit()
        print("Hr Approval ", user.hr_approval)
        print("Status ", user.status)
        emit('leave_hr_approval_update', {'userId': userID, 'hr_approval': user.hr_approval}, broadcast=True)

@views.route('/late_decline',methods=['POST','GET'])
def late_decline():
    user = json.loads(request.data)
    userID = user['userId']
    user = late.query.filter_by(emp_id=userID).first()
    print(" USER : ",user)
    current_user='hr'
    if current_user=='hr':
        user.hr_approval='Declined'
        user.status='Declined'
        db.session.commit()
        print("Hr Approval ", user.hr_approval)
        print("Status ", user.status)
        emit('late_hr_approval_update', {'userId': userID, 'hr_approval': user.hr_approval}, broadcast=True)

@views.route('/leave_decline',methods=['POST','GET'])
def leave_decline():
    user = json.loads(request.data)
    userID = user['userId']
    user = leave.query.filter_by(emp_id=userID).first()
    print(" USER : ",user)
    current_user='hr'
    if current_user=='hr':
        user.hr_approval='Declined'
        user.status='Declined'
        db.session.commit()
        print("Hr Approval ", user.hr_approval)
        print("Status ", user.status)
        emit('leave_hr_approval_update', {'userId': userID, 'hr_approval': user.hr_approval}, broadcast=True)

@socketio.on('late')
def handle_lateform_callback(lateDet):
    emp_id=lateDet['emp_id']
    emp_name=lateDet['emp_name']
    reason=lateDet['reason']
    from_time=lateDet['from_time']
    to_time=lateDet['to_time']
    status='Pending'
    hod_approval='Pending'
    approved_by='Hod Name'
    hr_approval='Pending'
    try:
        new_request=late(emp_id=emp_id,emp_name=emp_name,reason=reason,from_time=from_time,to_time=to_time,status=status,hod_approval=hod_approval,approved_by=approved_by,hr_approval=hr_approval)
        db.session.add(new_request)
        db.session.commit()
        print("new request : ",new_request.emp_id)
        all_latedata = {'emp_id':emp_id, 'emp_name':emp_name, 'reason':reason, 'from_time':from_time, 'to_time':to_time, 'status':status, 'hod_approval':hod_approval, 'approved_by':approved_by, 'hr_approval':hr_approval}
        print("EMP ID : ",all_latedata['emp_id'])

        emit('late', all_latedata, broadcast=True)


    except Exception as e:
        print(f"An error occurred: {str(e)}")



@views.route('/request_disp')
def request_disp():
    late_permission=late.query.order_by(late.date).all()
    leave_permission=leave.query.order_by(leave.date).all()
    return render_template('request_disp.html',late_permission=late_permission,leave_permission=leave_permission)

@socketio.on('leave')
def handle_leaveform_callback(leaveDet):
    emp_id=leaveDet['emp_id']
    emp_name=leaveDet['emp_name']
    reason=leaveDet['reason']
    from_date=leaveDet['from_date']
    to_date=leaveDet['to_date']
    status='Pending'
    hod_approval='Pending'
    approved_by='Hod Name'
    hr_approval='Pending'
    try:
        new_request=leave(emp_id=emp_id,emp_name=emp_name,reason=reason,from_date=from_date,to_date=to_date,status=status,hod_approval=hod_approval,approved_by=approved_by,hr_approval=hr_approval)
        db.session.add(new_request)
        db.session.commit()
        all_leaveData={'emp_id':emp_id,'emp_name':emp_name,'reason':reason,'from_date':from_date,'to_date':to_date,'status':status,'hod_approval':hod_approval,'approved_by':approved_by,'hr_approval':hr_approval}
        print(all_leaveData)
        emit('leave', all_leaveData, broadcast=True)


    except Exception as e:
        print(f"An error occurred: {str(e)}")



@views.route('/upload_csv',methods=['POST','GET'])
def upload_csv():
    if request.method == 'POST':
        if 'csvFile' not in request.files:
            return "No file part"

        file = request.files['csvFile']

        if file.filename == '':
            return "No selected file"

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            print(filename)
            file.save(os.path.join(app.config['EXCEL_FOLDER'], filename))
           
            # Create a new database record with file name and current datetime
            now = datetime.now()
            current_time = now.strftime("%Y-%m-%d %H:%M:%S")
            data = NewShift(
                name_date_day=f"File Uploaded on {current_time}",
                filename=filename  # Add the filename to the database
            )
            db.session.add(data)
            db.session.commit()
           
            return "File uploaded successfully"
        else:
            return "File not allowed"

    # If the request method is GET, render the upload form
    return render_template('upload_csv.html')


@views.route('/process_csv', methods=['POST','GET'])
def process_csv():
    # Query the database to get the latest uploaded record
    latest_data = NewShift.query.order_by(desc(NewShift.id)).first()
    
    if not latest_data:
        return "No files have been uploaded yet."
    
    latest_filename = latest_data.filename
    csv_filepath = os.path.join(app.config['EXCEL_FOLDER'], latest_filename)

    with open(csv_filepath, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)

        # Skip the first row containing headers
        next(csv_reader)  # Skip the first row

        # Read the second row which contains the days of the week (Monday to Friday)
        days_of_week = next(csv_reader)[2:]  # Assuming the first two columns are E.ID and Employee Name

        for row in csv_reader:  # Reading the employee's data rows
            employee_id = row[0]
            employee_name = row[1]
            shifts = row[2:]

            # Combine the days of the week with the shifts
            combined_shifts = days_of_week + shifts

            # Here you can process the employee data and store it in the database
            data_entry = NewShift(
                name_date_day=employee_name,
            )

            # Map the combined shifts to corresponding day columns dynamically
            for day_num, shift in enumerate(combined_shifts, start=1):
                setattr(data_entry, f"day_{day_num}", shift)

            db.session.add(data_entry)

        db.session.commit()

    return f"CSV data from {latest_filename} processed and stored in the database."

@views.route('/del_csv')
def del_csv():
    db.session.query(user).delete()
    db.session.commit()
    return redirect(url_for('upload_csv'))