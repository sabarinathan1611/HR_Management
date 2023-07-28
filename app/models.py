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
   
class Employee(db.Model,UserMixin):
    
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(150),nullable=False)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    dob = db.Column(db.DateTime(timezone=True))   
    # salary=db.Column(db.String(150))
    workType=db.Column(db.String(150))
    phoneNumber=db.Column(db.Integer)
    adharNumber=db.Column(db.Integer)
    gender = db.Column(db.String(150))
    address=db.Column(db.String(150))
    profile_pic = db.Column(db.String(100000), default='Default/Default.jpeg')
    attendance = db.relationship('Attendance')
    

class Attendance(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    emp_id = db.Column(db.Integer, db.ForeignKey('employee.id'))
    attendance =db.Column(db.String(150))
    inTime=db.Column(db.String(150))
    outTime=db.Column(db.String(150))
    overtime=db.Column(db.String(150))
    date = db.Column(db.DateTime(timezone=True), default=func.now())

    
    
    
    
    
    
