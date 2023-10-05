# main.py
from app import create_app, socketio

if __name__ == '__main__':
    app = create_app()
    socketio.init_app(app)  # Initialize socketio with the app
    socketio.run(app, debug=True)
