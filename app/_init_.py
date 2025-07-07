from flask import Flask
from app.models import init_db

def create_app():
    app = Flask(__name__)
    app.secret_key = 'your-secret-key'
    init_db()

    from app.main import main
    app.register_blueprint(main)

    return app
