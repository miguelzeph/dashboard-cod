from flask import Blueprint, render_template
# from mongo.mongo import updating_codename
# from utils.report import process_report_general
# from utils.data_tools import process_documents, display_function
# from utils.pagination_tools import process_pagination
# from utils.filter_panel_tools import filter_documents
# from utils.search_tools import perform_search, get_slider_range

trending = Blueprint(name="trending", import_name=__name__)

@trending.route("/trending/", methods=["GET", "POST"])
def index() -> str:
    """Starting index page"""
    return render_template("trending/index.html")
