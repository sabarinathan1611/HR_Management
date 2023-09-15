from app import create_app
from app import funcations
import datetime
import sched
import time
from datetime import datetime, timedelta


app, socketio = create_app()  
with app.app_context():
    if __name__ == '__main__':
        # Run the scheduler in a separate thread
        # from threading import Thread
        # scheduler_thread = Thread(target=funcations.scheduler.run)
        # scheduler_thread.start()
        # Create both app and socketio instances
        socketio.run(app, debug=True)  # Use socketio.run to run the application


 
    
