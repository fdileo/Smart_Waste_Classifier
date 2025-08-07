from flask import Flask
from .config import Configuration
from app.database import db
from flask_login import LoginManager
from bson import ObjectId


def create_app():
    
    app = Flask(__name__)
    app.config.from_object(Configuration)
    
    db.init_db(app)
    
    from .auth.routes import auth
    from .main.routes import main
    from .use_app.routes import application
    
    app.register_blueprint(main, url_prefix = '/')
    app.register_blueprint(auth, url_prefix = '/')
    app.register_blueprint(application, url_prefix = '/')
    
    from app.database.users import User
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(user_id):
        user_data = db.users_collection.find_one({"_id": ObjectId(user_id)})
        if user_data:
            return User(user_data)
        return None
    
    
    return app 