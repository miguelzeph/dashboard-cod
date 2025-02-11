from flask import Blueprint, render_template

portal = Blueprint(name="portal", import_name=__name__)

@portal.route("/", methods=["GET", "POST"])
def index() -> str:
    """Starting index page"""
    return render_template("portal/index.html")
