import os

from flask import Flask

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_session import Session


from splent_framework.core.managers.feature_manager import FeatureManager
from splent_framework.core.managers.config_manager import ConfigManager
from splent_framework.core.managers.error_handler_manager import ErrorHandlerManager
from splent_framework.core.managers.logging_manager import LoggingManager
from splent_framework.core.configuration.configuration import get_app_version
from splent_cli.utils.path_utils import PathUtils

db = SQLAlchemy()
migrate = Migrate(directory=PathUtils.get_migrations_dir())
mail_service = None
sess = Session()


def create_app(config_name="development"):
    app = Flask(__name__)

    # Load configuration according to environment
    config_manager = ConfigManager(app)
    config_manager.load_config(config_name=config_name)

    # Initialize SQLAlchemy and Migrate with the app
    db.init_app(app)
    migrate.init_app(app, db)

    # Initialize session with the app
    sess.init_app(app)

    # Register features
    feature_manager = FeatureManager(app)
    feature_manager.register_features()

    # Register login manager
    from flask_login import LoginManager
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    @login_manager.user_loader
    def load_user(user_id):
        from splent_feature_auth.models import User

        return User.query.get(int(user_id))

    # Set up logging
    logging_manager = LoggingManager(app)
    logging_manager.setup_logging()

    # Initialize error handler manager
    error_handler_manager = ErrorHandlerManager(app)
    error_handler_manager.register_error_handlers()

    from splent_feature_mail.services import MailService
    mail_service = MailService()
    mail_service.init_app(app)

    # Injecting environment variables into jinja context
    @app.context_processor
    def inject_vars_into_jinja():

        # Get all the environment variables
        env_vars = {key: os.getenv(key) for key in os.environ}

        # Add the application version manually
        env_vars["APP_VERSION"] = get_app_version()

        # Ensure DOMAIN variable has a default value if not set
        env_vars["DOMAIN"] = os.getenv("DOMAIN", "localhost")

        # Set Boolean variables for the environment
        flask_env = os.getenv("FLASK_ENV")
        env_vars["DEVELOPMENT"] = flask_env == "development"
        env_vars["PRODUCTION"] = flask_env == "production"

        return env_vars

    return app


def get_db():
    return db

__all__ = ["create_app", "get_db", "db", "mail_service"]
