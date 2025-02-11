from typing import Any
from flask import Blueprint, render_template, request, session, url_for, redirect, send_file

from mongo.mongo import updating_codename
from utils.report import process_report_general
from utils.data_tools import process_documents, display_function
from utils.pagination_tools import process_pagination
from utils.filter_panel_tools import filter_documents
from utils.search_tools import perform_search, get_slider_range

dashboard = Blueprint(name="dashboard", import_name=__name__)
status_panel_filter = ["TP", "FP", "PUBCHEM", "NO_PUBCHEM"]

@dashboard.route("/dashboard/", methods=["GET", "POST"])
def index() -> str:
    """Starting index page"""
    return render_template("dashboard/index.html")

@dashboard.route("/dashboard/report_general", methods=["GET", "POST"])
def report_general() -> str:
    
    process_report_general()
    
    # return redirect(url_for("dashboard.index", report=True))
    return render_template(
        "dashboard/report_general.html",
        report = True,
        chart_date_TP =  session.get("chart_date_TP"),
        chart_count_TP = session.get("chart_count_TP"),
        chart_count_FP = session.get("chart_count_FP"),
        chart_count_FP_least = session.get("chart_count_FP_least")
    )

# I had to separate the report into two view functions
# because it was losing formatting due to Pandas_Profiling
# So I put all into <iframe> 
@dashboard.route("/dashboard/report_pandas_profiling", methods=["GET", "POST"])
def report_pandas_profiling() -> str:
       
    return render_template(
        "dashboard/includes/includes_report/pandas_profiling.html",
        report_html=session["report_html"],
    )
    # return render_template(get_report_html())
    # return render_template("index.html", report = get_report_html())
    # return redirect(url_for("dashboard.index", report =get_report_html()))

@dashboard.route("/dashboard/filter/<show>", methods=["POST"])
def filter_codename(show: str) -> Any:

    if request.method == "POST":
        # Status
        checkbox = request.form.getlist("filter_checkbox")
        # Years Values
        slider = request.form.getlist("filter_slider")
        if slider:
            vals = [int(val) for val in slider[0].split(",")]
            slider_vals = {"min": min(vals), "max": max(vals)}
        else:
            slider_vals = {}

        session["status_filter"] = checkbox
        documents = filter_documents(session["documents"], checkbox, slider_vals)
        session[f"doc_{show}"] = process_documents(documents)
        session["slider_vals"] = slider_vals
        # session["slider"] = (
        #     get_min_max_year(session[f"doc_{show}"].get("data_list"))
        #     if session[f"doc_{show}"]
        #     else None
        # )

    return redirect(url_for("dashboard.search", show=show))


@dashboard.route("/dashboard/display_codename/<show>")
def display_codename(show: str) -> Any:
    """Filter data between:

    Args:
        show (string): TOTAL (all data); TP ( True Positives); FP (False Positives); PUBCHEM (codenames found on PubChem)

    Returns:
        Return nothing, just save the data in session and redirect to 'search' view function
    """

    if show != "TOTAL":
        session[f"doc_{show}"] = display_function(session["doc_TOTAL"], show)

    return redirect(url_for("dashboard.search", show=show))


@dashboard.route("/dashboard/reset/", methods=["GET", "POST"])
def reset_filter() -> Any:
    
    session["status_filter"] = status_panel_filter
    session["doc_TOTAL"] = process_documents(session["documents"])
    session["slider"] = get_slider_range(session["doc_TOTAL"])
    session["slider_vals"] = session["slider"]

    return redirect(url_for("dashboard.search", show="TOTAL"))


@dashboard.route("/dashboard/search/<show>", methods=["GET", "POST"])
def search(show: str) -> str:
    """Search for codename in database"""

    if request.method == "POST":
        session["status_filter"] = status_panel_filter
        search_results = perform_search()

        session["documents"] = search_results["documents"]
        session[f"doc_{show}"] = process_documents(search_results["documents"])

        session["slider"] = get_slider_range(session[f"doc_{show}"])
        session["slider_vals"] = session["slider"]

    docs_processed = session[f"doc_{show}"]
    
    if docs_processed:
        pagination_data, pagination = process_pagination(docs_processed)

        return render_template(
            "dashboard/result.html",
            pagination_data=pagination_data,
            pagination=pagination,
            total_found=docs_processed["total_found"],
            counter=docs_processed["counter_field_TP"],
            show=show,
            years_min_max=session.get("slider"),
            years_vals=session.get("slider_vals"),
            drug_name=session["drug_name"],
            filter_status=session.get("status_filter"),
            total_chart =docs_processed["total_chart"]
        )

    return render_template(
        "dashboard/codename_not_found.html",
        show=show,
        codename_not_found=request.form.get("drug_name"),
        searched_by_pmid= request.files.get("file_upload").filename if request.files.get("file_upload") else None
    )


@dashboard.route("/dashboard/save_mongo", methods=["POST"])
def save_mongo() -> Any:
    """Save data on MongoDB (background process happening without any refreshing)

    Returns:
        Nothing
    """

    values = request.values

    obj = {
        "codename": values["synonym"], # Fix synonym on html form to codename
        "comment": values["comment"] if values["comment"] else None,
        "class": values["class"].title().replace(" ", "_") if values["class"] else None,
        "true_positive": values["TP"].lower() in ["true", "1"],
        "validated_by_pipeline": False,
    }

    updating_codename(obj)

    return ("Saved!", 200)


@dashboard.route("/dashboard/download")
def download_file() -> Any:
    """Download the file in csv format

    Returns:
        Return the csv file with following information
        codename | compound_id | true_positive | in_pubchem | pubmed_count
    """

    path, filename = "./", "pubmed_dashboard_file.csv"
    with open(f"{path}/{filename}", "w", encoding="utf-8") as f:
        # f.write("codename\tcompound_id\ttrue_positive\tin_pubchem\tpubmed_count\tpmid\ttitle\tabstract\n")
        f.write("pmid\tcodename\tjournal\tcompound_id\ttrue_positive\tin_pubchem\tpubmed_count\n")


        for data in session["doc_TOTAL"]["data_list"]:
            article = data['first_element_article']
            # {data['list_pmid']}
            # write = f"{data['codename']}\t{data['compound_id']}\t{data['TP']}\t{data['in_pubchem']}\t{data['pubmed_count_results']}\t{article['pmid']}\t{article['title']}\t{article['abstract']}\n"
            write = f"{article['pmid']}\t{data['codename']}\t{article['journal']}\t{data['compound_id']}\t{data['TP']}\t{data['in_pubchem']}\t{data['pubmed_count_results']}\n"
            f.write(write)

    return send_file(filename, as_attachment=True)