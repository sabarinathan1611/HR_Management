from app import create_app
from auth import schedule_next_sunday,scheduler

app= create_app()


if __name__ == '__main__':
    app.run(debug=True,port=5500)
    # Schedule the function to run for the first time
    schedule_next_sunday()

    # Run the scheduler loop
    scheduler.run()