from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from config import Config_options
from flask_login import LoginManager
from flask_uploads import UploadSet, configure_uploads
from flask_bootstrap import Bootstrap

db = SQLAlchemy()
mail = Mail()
bootstrap = Bootstrap()

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'
photos = UploadSet('photos', )


def create_app(config_name):
    app = Flask(__name__)

    # app configuration

    app.config.from_object(Config_options[config_name])

    # register blueprint
    from .main import main  as main_blueprint
    app.register_blueprint(main_blueprint)
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/authenticate')

    # Initializing Flask Extensions
    bootstrap.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    # configure UploadSet
    configure_uploads(app, photos)

    return app
