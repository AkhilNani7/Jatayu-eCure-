import os
import logging

from flask import Flask
from flask_login import LoginManager
from extensions import db  # Import db from extensions

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key")

# Configure the database
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///healthapp.db")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

# Initialize the app with the extensions
db.init_app(app)

# Setup LoginManager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

with app.app_context():
    # Import and register blueprints/routes after the db is initialized
    from routes import init_routes
    init_routes(app, db)

    # Setup login manager loader
    from models import User
    
    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))