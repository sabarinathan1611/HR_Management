from flask_login import login_required, current_user,login_user
from . import db
from .models import Employee,Attendance,Shift_time,Backup, late, leave,notification,NewShift,Emp_login
from flask import Blueprint, render_template, request, flash, redirect, url_for,jsonify,session
import json
import datetime
import pandas as pd
from flask import current_app as app
from datetime import datetime, timedelta
import os
from werkzeug.security import generate_password_hash, check_password_hash
from .funcations import *
from werkzeug.utils import secure_filename
from sqlalchemy.exc import SQLAlchemyError


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
def admin():     # not used ,,,, used in auth itself
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
    late_permission=late.query.order_by(late.date).all()
    leave_permission=leave.query.order_by(leave.date).all()
    # sihft=Shift_time.query.order_by(Shift_time.id) 
    return render_template('admin.html',employee=employee,late_permission=late_permission,leave_permission=leave_permission)

@views.route('/edit', methods=['POST', 'GET'])
@login_required
def empEdit():
    if request.method == 'POST':
        empid = session.get('emp_id')
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

        # Redirect the user _to the 'admin' page or route.
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
    attendance=Attendance.query.all()
    
    return render_template("admin.html",attendance=attendance)
            
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

@socketio.on('late')
@login_required
def handle_lateform_callback(lateDet):
    emp_id=session.get('emp_id')
    emp_name=session.get('name')
    reason=lateDet['reason']
    from_time=lateDet['from_time']
    to_time=lateDet['to_time']
    status='Pending'
    hod_approval='Pending'
    approved_by='Hod Name'
    hr_approval='Pending'

    user=Emp_login.query.filter_by(emp_id=emp_id).first()
    if user:
        user.late_balance -= 1
        email=user.email
        late_balance=user.late_balance
        db.session.commit()
    
    else:
        print(f"Employee with emp_id {emp_id} not found.")
    user=Emp_login.query.filter_by(emp_id=emp_id).first()
    if user:
        email=user.email
        try:
            sub=" You Have Taken Late Permission "
            body=" You Have Taken Late permission \n And You Have {} Late balance \n Have a Great Day".format(late_balance)
            send_mail(email, sub, body)
        except:
            print("Mail Not Sent")

    try:
        user=Employee.query.filter_by(emp_id=emp_id).first()
        phone=user.phoneNumber
        body=" You Have Taken Late permission \n And You Have {} Late balance \n Have a Great Day".format(late_balance)
        send_sms(phone,body)
    except:
        print("Sms Not Sent")

    try:
        print(reason)
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
    emp_id=session.get('emp_id')
    emp_name=session.get('name')
    reason=leaveDet['reason']
    from_date=leaveDet['from_date']
    to_date=leaveDet['to_date']
    status='Pending'
    hod_approval='Pending'
    approved_by='Hod Name'
    hr_approval='Pending'

    user=Emp_login.query.filter_by(emp_id=emp_id).first()
    if user:
        user.leave_balance -= 1
        email=user.email
        leave_balance=user.leave_balance
        db.session.commit()
    else:
        print(f"Employee with emp_id {emp_id} not found.")
    user=Emp_login.query.filter_by(emp_id=emp_id).first()
    if user:
        email=user.email
        try:
            sub=" You Have Taken Leave "
            body=" You Have Taken Leave \n And You Have {} Leave balance \n Have a Great Day".format(leave_balance)
            send_mail(email, sub, body)
        except:
            print("Mail Not Sent")

        try:
            user=Employee.query.filter_by(emp_id=emp_id).first()
            phone=user.phoneNumber
            phone="+91"+phone
            print(type(phone))
            body=" You Have Taken leave permission \n And You Have {} leave balance \n Have a Great Day".format(leave_balance)
            send_sms([phone],body)
        except:
            print("Sms Not Sent")

    try:
        new_request=leave(emp_id=emp_id,emp_name=emp_name,reason=reason,from_date=from_date,to_date=to_date,status=status,hod_approval=hod_approval,approved_by=approved_by,hr_approval=hr_approval)
        db.session.add(new_request)
        db.session.commit()
        all_leaveData={'emp_id':emp_id,'emp_name':emp_name,'reason':reason,'from_date':from_date,'to_date':to_date,'status':status,'hod_approval':hod_approval,'approved_by':approved_by,'hr_approval':hr_approval}
        print(all_leaveData)
        emit('leave', all_leaveData, broadcast=True)

    except Exception as e:
        print(f"An error occurred: {str(e)}")

@views.route('/upload_csv_page',methods=['POST','GET'])
def upload_csv_page():
    return render_template("upload_csv.html")

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
            file_path=os.path.join(app.config['EXCEL_FOLDER'], filename)
            file.save(file_path)
            process_csv_file(file_path)
                # # Create a new database record with file name and current datetime
                # now = datetime.now()
                # current_time = now.strftime("%Y-%m-%d %H:%M:%S")
                # data = NewShift(
                #     name_date_day=f"File Uploaded on {current_time}",
                #     filename=filename  # Add the filename to the database
                # )
                # db.session.add(data)
                # db.session.commit()
            
            return redirect(url_for('views.process_csv'))
        else:
            return "File not allowed"
    # I the request method is GET, render the upload form
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
    db.session.query(NewShift).delete()
    db.session.commit()
    return redirect(url_for('upload_csv'))

def process_csv_file(file_path):
    with open(file_path, mode='r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skip the header row

        for row in csv_reader:
            employee_id, employee_name, *shifts = row

            # Create a new NewShift instance and set its attributes
            new_shift_entry = NewShift(
                name_date_day=employee_name,
                filename=file_path,
                monday=shifts[0],
                tuesday=shifts[1],
                wednesday=shifts[2],
                thursday=shifts[3],
                friday=shifts[4]
            )

            # Set the day_* attributes dynamically
            for day_num, shift in enumerate(shifts[5:], start=1):
                setattr(new_shift_entry, f"day_{day_num}", shift)

            # Add the new entry to the database session
            db.session.add(new_shift_entry)

        # Commit the changes to the database
        db.session.commit()

@views.route("/emp_login_page")
def emp_login_page():
    return render_template("emp_log.html")

@views.route("/emp_login",methods=['POST','GET'])
def emp_login():
    if request.method == 'POST':
        emp_id = request.form.get('emp_id') # Get the emp_id from the form
        password = request.form.get('password')  # Get the password from the form

        # Store the email and password in session variables
        
        user = Emp_login.query.filter_by(emp_id=emp_id).first()
        if user:
            if user.password == password:
                login_user(user, remember=True)
                session['emp_id'] = emp_id
                session['password'] = password
                session['name'] = user.name
                session['email'] = user.email
                session['leave_balance']=user.leave_balance
                session['late_balance']=user.late_balance
                return redirect(url_for('views.user_dashboard'))
            else:
                flash("Incorrect Password", category='error')
        else:
            flash("Incorrect Employee ID", category='error')
    return render_template("emp_log.html")

@views.route("/user_dashboard",methods=['POST','GET'])
def user_dashboard():
    if current_user.role=="admin":
        return redirect(url_for('auth.logout'))
    emp_id = session.get('emp_id')
    email = session.get('email')
    name = session.get('name')
    user = Emp_login.query.filter_by(emp_id=emp_id).first()
    leave_balance = user.leave_balance
    late_balance = user.late_balance
    return render_template("emp_req_choice.html",emp_id=emp_id,email=email,name=name,late_balance=late_balance,leave_balance=leave_balance)

@views.route("/attendance_upload_page",methods=['POST','GET'])
def attendance_upload_page():
    return render_template('upload_attendance.html')

@views.route("/attendance_upload",methods=['POST','GET'])
def upload_attendance():
    if request.method=='POST':
        file=request.files['attendance']
        filename = secure_filename(file.filename)
        print(filename)
        file_path=os.path.join(app.config['EXCEL_FOLDER'], filename)
        file.save(file_path)
        process_excel_data(file_path)
        print("SUccess ")
        return redirect(url_for('views.calculate'))

    else:
        return redirect(url_for('views.attendance_upload_page'))

@views.route("/attendance_table")
@login_required
def attendance_table():
    late_permission=late.query.order_by(late.date).all()
    leave_permission=leave.query.order_by(leave.date).all()
    return render_template("admin.html",late_permission=late_permission,leave_permission=leave_permission)

@views.route("/late_table")
@login_required
def late_table():
    late_permission=late.query.order_by(late.date).all()
    return render_template("late_table.html",late_permission=late_permission)

@views.route("/leave_table")
@login_required
def leave_table(): 
    leave_permission=leave.query.order_by(leave.date).all()
    return render_template("leave_table.html",leave_permission=leave_permission)

@views.route("/today_attendance")
@login_required
def today_attendance():
    return render_template("admin.html")

@views.route("/yesterday_attendance")
@login_required
def yesterday_attendance():
    return render_template("admin.html")

@views.route("/month_attendance")
@login_required
def month_attendance():
    return render_template("month_attendance.html")

@views.route("/last_month_attendance")
@login_required
def last_month_attendance():
    return render_template("month_attendance.html")

@views.route('/late_req_profile/<int:emp_id>/<string:emp_name>/<string:from_time>/<string:to_time>/<string:reason>/<int:req_id>')
def late_req_profile(emp_id, emp_name, from_time, to_time, reason,req_id):
    user = Emp_login.query.order_by(Emp_login.date.desc()).first()
    user_late=late.query.filter_by(id=req_id).first()
    late_details={
        'late_balance':user.late_balance,
        'leave_balance':user.leave_balance,
        'approval':user_late.hr_approval,
        'from_time':from_time,
        'to_time':to_time,
        'approved_by':user_late.approved_by,
        'ph_number':user.phoneNumber,
        'id':user.id,
        'reason':reason,
        'emp_id':emp_id,
        'emp_name':emp_name
    }
    session['late_details']=late_details
    return render_template("late_req_profile.html",late_details=late_details)#,late_permission_dict=late_permission_dict

@views.route('/leave_req_profile/<int:emp_id>/<string:emp_name>/<string:from_date>/<string:to_date>/<string:reason>/<int:req_id>')
def leave_req_profile(emp_id, emp_name, from_date, to_date, reason,req_id):
    user = Emp_login.query.order_by(Emp_login.date.desc()).first()
    user_leave=leave.query.filter_by(id=req_id).first()
    leave_details={
        'leave_balance':user.leave_balance,
        'leave_balance':user.leave_balance,
        'approval':user_leave.hr_approval,
        'approved_by':user_leave.approved_by,
        'from_date':from_date,
        'to_date':to_date,
        'ph_number':user.phoneNumber,
        'id':user.id,
        'reason':reason,
        'emp_id':emp_id,
        'emp_name':emp_name
    }
    session['leave_details']=leave_details
    return render_template("leave_req_profile.html",leave_details=leave_details)#,late_permission_dict=late_permission_dict

# @views.route('/late_req_approve',methods=['POST','GET'])
# def late_req_approve():
#     late_details=session.get('late_details')
#     return render_template("late_req_profile.html",late_details=late_details)

# @views.route('/late_req_decline',methods=['POST','GET'])
# def late_req_decline():
#     late_details=session.get('late_details')
#     return render_template("late_req_profile.html",late_details=late_details)

# @views.route('/leave_approve',methods=['POST','GET'])
# def leave_approve():
#     user = json.loads(request.data)
#     userID = user['userId']
#     user = leave.query.filter_by(emp_id=userID).first()
#     print(" USER : ",user)
#     current_user='hr'
#     if current_user=='hr':
#         user.hr_approval='Approved'
#         user.approved_by=userID
#         db.session.commit()
#         print("Hr Approval ", user.hr_approval)
#         print("Status ", user.status)
#         emit('leave_hr_approval_update', {'userId': userID, 'hr_approval': user.hr_approval}, broadcast=True)

# @views.route('/leave_decline',methods=['POST','GET'])
# def leave_decline():
#     user = json.loads(request.data)
#     userID = user['userId']
#     user = leave.query.filter_by(emp_id=userID).first()
#     print(" USER : ",user)
#     current_user='hr'
#     if current_user=='hr':
#         user.hr_approval='Declined'
#         user.status='Declined'
#         db.session.commit()
#         print("Hr Approval ", user.hr_approval)
#         print("Status ", user.status)
#         emit('leave_hr_approval_update', {'userId': userID, 'hr_approval': user.hr_approval}, broadcast=True)

@views.route('/late_approve', methods=['POST', 'GET'])
def late_approve():
    user_data = json.loads(request.data)
    userID = user_data['userId']
    user = late.query.filter_by(emp_id=userID).first()
    current_user = 'hr'
    
    if current_user == 'hr':
        user.hr_approval = 'Approved'
        user.approved_by=userID
        db.session.commit()
        
        # Create a JSON response
        response_data = {
            'approved_by':user.approved_by,
            'userId': userID,
            'hr_approval': user.hr_approval
        }

        return jsonify(response_data)

@views.route('/late_decline', methods=['POST', 'GET'])
def late_decline():
    user_data = json.loads(request.data)
    userID = user_data['userId']
    user = late.query.filter_by(emp_id=userID).first()
    current_user = 'hr'
    if current_user == 'hr':
        user.hr_approval = 'Declined'
        user.approved_by=userID
        db.session.commit()
        
        # Create a JSON response
        response_data = {
            'approved_by':user.approved_by,
            'userId': userID,
            'hr_approval': user.hr_approval
        }

        return jsonify(response_data)


@views.route('/leave_approve',methods=['POST','GET'])
def leave_approve():
    user_data = json.loads(request.data)
    userID = user_data['userId']
    user = leave.query.filter_by(emp_id=userID).first()
    print(" USER : ",user)
    current_user='hr'
    if current_user=='hr':
        user.hr_approval='Approved'
        user.approved_by=userID
        db.session.commit()
        response_data = {
            'approved_by':user.approved_by,
            'userId': userID,
            'hr_approval': user.hr_approval
        }

        return jsonify(response_data)

@views.route('/leave_decline',methods=['POST','GET'])
def leave_decline():
    user = json.loads(request.data)
    userID = user['userId']
    user = leave.query.filter_by(emp_id=userID).first()
    print(" USER : ",user)
    current_user='hr'
    if current_user=='hr':
        user.hr_approval='Declined'
        user.approved_by=userID
        db.session.commit()
        response_data = {
            'approved_by':user.approved_by,
            'userId': userID,
            'hr_approval': user.hr_approval
        }

        return jsonify(response_data)