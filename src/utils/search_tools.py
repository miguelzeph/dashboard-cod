from flask import request, session
from app.config_dashboard import n_report_f

from mongo.mongo import search_for_drug_name, search_for_pmid, search_for_drug_name_list
from utils.file_tools import get_pmid_list
from utils.data_tools import get_min_max_year


def perform_search():
    """Search for drug name or file with pmid"""

    newest_codename = request.form.get("newest_codename")
    count_codename_TP = request.form.get("count_codename_TP")
    count_codename_FP = request.form.get("count_codename_FP")
    count_codename_FP_least = request.form.get("count_codename_FP_least")
    file = request.files.get("file_upload")
    # File
    if file:
        pmid_list = get_pmid_list(file=file)
        documents = search_for_pmid(pmid_list=pmid_list)
        drug_name = f"File List ({len(pmid_list)})"
        # session["searched_by_pmid"] = file.filename
    # 100 newest codename
    elif newest_codename:
        drug_name_list = session["newest_codename"]
        documents = search_for_drug_name_list(drug_name_list)
        drug_name = f"{n_report_f} Newest Codename"
    # 100 most counted codename
    elif count_codename_TP:
        drug_name_list = session["count_codename_TP"]
        documents = search_for_drug_name_list(drug_name_list)
        drug_name = f"Top-{n_report_f} Codename (TP)"
    elif count_codename_FP:
        drug_name_list = session["count_codename_FP"]
        documents = search_for_drug_name_list(drug_name_list)
        drug_name = f"Top-{n_report_f} Codename (TP)"
    elif count_codename_FP_least:
        drug_name_list = session["count_codename_FP_least"]
        documents = search_for_drug_name_list(drug_name_list)
        drug_name = f"{n_report_f} Least Counted Codename FP"
    # Drugname
    else:
        drug_name = request.form.get("drug_name")
        documents = search_for_drug_name(drug_name)

    session["drug_name"] = drug_name

    return {"documents": documents}


def get_slider_range(documents):
    """Return the range of years for the slider"""
    if documents:
        data_list = documents.get("data_list")
        if data_list:
            return get_min_max_year(data_list)
    return None