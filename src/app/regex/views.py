import re
from flask import Blueprint, render_template, request

from codename_hunter.parse.regex_code import pattern_list
from codename_hunter.utils.create_regex import CreateRegex
from codename_hunter.mongo.mongo import populate_regex_db
from mongo.mongo import search_for_drug_name_regex

regex = Blueprint(name="regex", import_name=__name__)

@regex.route("/regex/", methods=["GET", "POST"])
def index() -> str:
    """Starting index page"""
    return render_template("regex/index.html")
    
@regex.route("/regex/result", methods=["GET", "POST"])
def check_regex() -> str:
    
    elements = []
    total_codename = 0
    for pattern in pattern_list:
        element = search_for_drug_name_regex(pattern)
        elements.append(element)
        
        if element.get("total"):
            total_codename+=element["total"]
    
    return render_template(
        "regex/result.html",
        elements = elements,
        total_codename=total_codename,
        total_pattern = len(pattern_list)
    )

@regex.route("/regex/ingest",methods=["POST"])
def ingest_codename():

    if request.method == "POST":
        
        file = request.files.get("codename_list")
        
        if file:
            text = file.read().decode("utf-8")
            
            # Get Codename List
            codename_list = [ codename for codename in text.strip(" |\n|\t|,|;").splitlines() if codename]
            
            ####  Check if it's a codename, if yes, create an pattern for this codename and populate pattern db. ####
            codenames_updated = []
            for codename in codename_list:
                status = "Not a codename"
                # Check if it's a codename (at least one Uppercase and Number)
                if re.match(r".*[A-Z].*\d.*", codename):
                    # Create Pattern
                    pattern = CreateRegex(codename).output()
                    # Populate Pattern Database
                    populate_regex_db(pattern, codename)
                    status = "Updated"
                    
                codenames_updated.append({"codename":codename,"status":status}) 
            ###########################################################################################################   
            
    return render_template(
        "regex/result.html",
        codenames_updated = codenames_updated
    )