from flask import Flask
from flask_sqlalchemy import  SQLAlchemy
from flask_login import LoginManager

db= SQLAlchemy()
DB_NAME="database.db"

def create_app():
    app= Flask(__name__)
    app.config['SECRET_KEY'] = '#$&^&^WYYDUHS&YWE'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}'.format(DB_NAME)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False
    
    db.init_app(app)
    
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USE_SSL'] = True
    
    from .auth import auth
    from .views import views
    app.register_blueprint(views,url_prefix='/')
    app.register_blueprint(auth,url_prefix='/')
    from.models import Login_admin,Employee,Attendance
    with app.app_context():
        db.create_all()
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    @login_manager.user_loader
    def load_user(id):
        return Login_admin.query.get(int(id))
    return app





def create_database(app):
    if not path.exists('app/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')
        
        


# Initialize the scheduler
scheduler = sched.scheduler(time.time, time.sleep)

def count_attendance_and_update_shift_periodic(emp_id):
    # Replace employee_id_to_check with the actual employee ID you want to check
    attendance_count = count_attendance_and_update_shift(emp_id)
    print(f"Attendance Count for Employee ID {emp_id}: {attendance_count}")

def schedule_next_sunday():
    # Calculate the time until the next Sunday
    now = datetime.now()
    days_until_sunday = (6 - now.weekday()) % 7  # Sunday is 6 in the Python datetime weekday representation
    next_sunday = now + timedelta(days=days_until_sunday)

    # Schedule the function to run on the next Sunday at midnight (00:00:00)
    next_sunday_midnight = datetime(next_sunday.year, next_sunday.month, next_sunday.day)
    scheduler.enterabs(time.mktime(next_sunday_midnight.timetuple()), 1, run_for_all_employees, ())

def run_for_all_employees():
    # Assuming Employee is your SQLAlchemy model for employees
    employees = Employee.query.filter_by(workType='desired_workType_value').all()

    for employee in employees:
        count_attendance_and_update_shift_periodic(employee.id)

    # Schedule the function to run again on the next Sunday
    schedule_next_sunday()

