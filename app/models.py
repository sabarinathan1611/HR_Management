from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Login_admin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150),nullable=False)
    email=db.Column(db.String(150),unique=True)
    password = db.Column(db.String(150))
    phoneNumber=db.Column(db.Integer)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
   
class Employee(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    dob = db.Column(db.DateTime(timezone=True))
    designation = db.Column(db.String(150), nullable=True)
    workType = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True)
    phoneNumber = db.Column(db.Integer)
    adharNumber = db.Column(db.Integer)
    gender = db.Column(db.String(150))
    address = db.Column(db.String(150))
    profile_pic = db.Column(db.String(100000), default='Default/Default.jpeg')
    attendance = db.relationship('Attendance', backref='employee')
    
    
class Attendance(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    emp_id = db.Column(db.Integer, db.ForeignKey('employee.id'))
    attendance =db.Column(db.String(150))
    wages_per_Day=db.Column(db.String(150))
    inTime=db.Column(db.String(150))
    outTime=db.Column(db.String(150))
    overtime=db.Column(db.String(150),default='00:00')
    shift=db.Column(db.String(150))
    
    TotalDuration=db.Column(db.String(150))
    lateBy=db.Column(db.String(150))
    earlyGoingBy=db.Column(db.String(150))
    punchRecords=db.Column(db.String(150))	
    

class Shift_time(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    shiftIntime = db.Column(db.String(150))
    shift_Outtime = db.Column(db.String(150))
    shiftType = db.Column(db.String(150))
    work_Duration=db.Column(db.String(150))
    
    
    
    
    
    
    
