from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Login_HR(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150),nullable=False)
    email=db.Column(db.String(150),unique=True)
    password = db.Column(db.String(150))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    
class Employee(db.Model,UserMixin):
    
    empid=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(150),nullable=False)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    attendance =db.Column(db.String(150))
    salary=db.Column(db.String(150))
    empType=db.Column(db.String(150))
    phoneNumber=db.Column(db.Integer)
   
