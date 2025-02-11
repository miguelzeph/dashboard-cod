from flask import session
import plotly.express as px
# from pandas_profiling import ProfileReport
from ydata_profiling import ProfileReport

from pandas import DataFrame
from app.config_dashboard import n_report_f, n_report_i

from mongo.mongo import get_data_report_count_codename, get_data_report_general

def get_report_general():
    
    data_report = get_data_report_general()
    df = DataFrame(data_report)
    
    ############## last 100 documents created into DB ###############

    # (use as a search -> see search_tools.py)
    session["newest_codename"] = list(df["codename"][n_report_i:n_report_f])
    df_date_TP = df[["created","true_positive"]][n_report_i:n_report_f]
    ######################################################################

    ############### Pandas Profiling Overview (CHART) ####################
    session["report_html"] = ProfileReport(
        df[
            [
                "in_pubchem",
                "pubmed_count_results",
                "true_positive",
                "validated_by_pipeline"
            ]
        ], 
        title = "Codename & Synonyms",
        # minimal=True
    ).to_html()
    #######################################################################

    ##################### 100 most repetead codenames (TP) ################
    data_report_count_TP = get_data_report_count_codename(
        true_positive=True,
        sort_count = -1
    )
    df_count_TP = DataFrame(data_report_count_TP)
    # (use as a search -> see search_tools.py)
    session["count_codename_TP"] = list(df_count_TP["codename"][n_report_i:n_report_f])

    ##################### 100 most counted codenames (FP) #################
    data_report_count_FP = get_data_report_count_codename(
        true_positive=False,
        sort_count = -1 # Most
    )
    df_count_FP = DataFrame(data_report_count_FP)
    # (use as a search -> see search_tools.py)
    session["count_codename_FP"] = list(df_count_FP["codename"][n_report_i:n_report_f])

    ##################### 100 least counted codenames (FP) #################
    data_report_count_FP_least = get_data_report_count_codename(
        true_positive=False,
        sort_count = +1 # Least
    )
    df_count_FP_least = DataFrame(data_report_count_FP_least)
    # (use as a search -> see search_tools.py)
    session["count_codename_FP_least"] = list(df_count_FP_least["codename"][n_report_i:n_report_f])

    return {
        "df_date_TP": df_date_TP,
        "df_count_TP":df_count_TP,
        "df_count_FP":df_count_FP,
        "df_count_FP_least":df_count_FP_least

    }

def process_report_general():

    report = get_report_general()
    
    # Charts config
    chart_size = {"width":600,"height":400}
    
    ####### Pass list of first 100 newest codename to other view #####  
    
    # Plot chart with 100 newest
    df = report["df_date_TP"]
    
    # Chat of TP & FP and Created Data
    color_map = {True:"blue", False:"red"}
    
    chart_date_TP = px.histogram(
        df,
        x="created",
        color="true_positive",
        nbins=len(df["created"].unique()),
        barmode="group",
        width=chart_size["width"],
        height=chart_size["height"],
        color_discrete_map=color_map,
        title= f"{n_report_f} Newest Codename Found TP"
    ).to_html()
    
    # Send chart to session
    session["chart_date_TP"] = chart_date_TP
    
    ################## Count Synonyms True Positive ##################
    chart_count_TP = px.bar(
        report["df_count_TP"][:n_report_f], 
        x="codename",
        y="count",
        width=chart_size["width"],
        height=chart_size["height"],
        title=f"Top-{n_report_f} Codename (TP)",
    ).to_html()
    session["chart_count_TP"] = chart_count_TP
    
    
    ################### Count Synonyms False Positive #################
    chart_count_FP = px.bar(
        report["df_count_FP"][:n_report_f], 
        x="codename",
        y="count",
        width=chart_size["width"],
        height=chart_size["height"],
        color_discrete_sequence=["red"],
        title=f"Top-{n_report_f} Codename (FP)",
    ).to_html()
    session["chart_count_FP"] = chart_count_FP
    
    ################### Count Synonyms False Positive (least) #################
    chart_count_FP_least = px.bar(
        report["df_count_FP_least"][:n_report_f], 
        x="codename",
        y="count",
        width=chart_size["width"],
        height=chart_size["height"],
        color_discrete_sequence=["red"],
        title=f"{n_report_f} Least Counted Codename FP",
    ).to_html()
    session["chart_count_FP_least"] = chart_count_FP_least

    return True