from flask import Flask
from flask_session import Session
from app.portal.views import portal
from app.dashboard.views import dashboard
from app.pipeline.views import pipeline
# from app.parse_text.views import parse_text
from app.trending.views import trending
# from app.regex.views import regex
from app.config_flask import config_flask

# from flask_jsglue import JSGlue

app = Flask(__name__, template_folder="./app/templates", static_folder="./app/static")

# Registering Features
app.register_blueprint(portal)
app.register_blueprint(dashboard)
app.register_blueprint(pipeline)
# app.register_blueprint(parse_text)
app.register_blueprint(trending)
# app.register_blueprint(regex)

# Configuration
config_flask(app) # Our personal config
Session(app) # Used to add Server-side Session to one or more Flask applications

# jsglue = JSGlue(app)
# print(app._static_folder)

# if __name__ == "__main__":

#     app.run(
#         host= str(config.get("flask.api_host")), # 0.0.0.0
#         port= config.get("flask.api_port"), # 5000
#         debug=True
#     )
