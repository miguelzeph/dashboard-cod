import json

from flask import Blueprint, render_template, request, session

from codename_hunter.parse_text import FindCodename, ValidateCodename


parse_text = Blueprint(name="parse_text", import_name=__name__)

@parse_text.route("/parse_text/", methods=["GET", "POST"])
def index() -> str:
    """Starting index page"""
    return render_template("parse_text/index.html")

@parse_text.route("/parse_text/result", methods=["GET","POST"])
def parsing_function():

    if request.method == "POST":

        # Raw text from search bar
        text = request.values["text_area"]
        # text = request.json.get("text_area")
        
        print(text)
        
        ######################### Parsing ########################
        # Find Codenames
        codenames = FindCodename(input_data=text).output()

        results = []
        highlight_TP = []
        highlight_FP = []
        for codename in codenames:

            # Validate Codenames
            result = ValidateCodename(
                    input_data=codename,
                    blacklist = [],
                    threshold_count = 150,
            ).output()
            
            
            results.append({
                    "codename": result,
                    "pretty_print": json.dumps(result, indent=4, separators=(",", ": "))
                } 
            )
            
            if result["true_positive"]:
                highlight_TP.append(result["codename"])
            else:
                highlight_FP.append(result["codename"])
        ###########################################################
                
        # Add in session
        session["text_area"] = text
        session["results"] = results
        session["highlight_words"] = {"TP_list":highlight_TP, "FP_list":highlight_FP}
                
        return render_template(
            "/parse_text/result.html",
            results = session["results"],
            text_area = session["text_area"],
            highlight_words= session["highlight_words"]

        )
    
    # Get
    return render_template(
        "/parse_text/result.html",
        results = session["results"],
        text_area = session["text_area"],
        highlight_words = session["highlight_words"]
    )
    