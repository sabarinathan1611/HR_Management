from flask_login import login_required, current_user
from . import db
from .models import Employee
from flask import Blueprint, render_template, request, flash, redirect, url_for

views = Blueprint('views', __name__)


@views.route('/admin',methods=['POST','GET'])
def admin():
    employee =Employee.query.order_by(Employee.id)
    return render_template('admin.html',employee=employee)
