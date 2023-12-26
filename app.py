# main.py
from app import create_app, socketio
from werkzeug.middleware.proxy_fix import ProxyFix

app = create_app()
socketio.init_app(app)  # Initialize socketio with the app

# Adding WSGI middleware (ProxyFix for Nginx)
app.wsgi_app = ProxyFix(app.wsgi_app)

if __name__ == '__main__':
    socketio.run(app, debug=True)
