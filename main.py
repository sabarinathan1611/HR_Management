from app import create_app
from app import funcations
import datetime
import sched
import time
from datetime import datetime, timedelta


app = create_app() 

if __name__ == '__main__':
    # Schedule the first task
   

    # Run the scheduler in a separate thread
    # from threading import Thread
    # scheduler_thread = Thread(target=funcations.scheduler.run)
    # scheduler_thread.start()
    # Run the Flask app
    app.run(debug=True, port=5500)
    
