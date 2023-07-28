from flask_login import login_required, current_user
from . import db
from .models import Employee
from flask import Blueprint, render_template, request, flash, redirect, url_for

views = Blueprint('views', __name__)


@views.route('/',methods=['POST','GET'])
def admin():
    employee =Employee.query.order_by(Employee.id)
    return render_template('admin.html',employee=employee)

@views.route('/edit',methods=['POST','GET'])
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
    
        
    
         