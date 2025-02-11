import os
from klein_config import get_config

config = get_config()

def config_flask(app):
    """Setup Flask environment variables

    Args:
        app : The flask object
    """
    app.config['UPLOAD_FOLDER'] = './static/upload'
    app.config["SECRET_KEY"] = config.get("flask.secret_key")
    app.config["SESSION_TYPE"] = config.get("flask.session_type")
    os.environ["FLASK_DEBUG"] = str(config.get("flask.debug"))
