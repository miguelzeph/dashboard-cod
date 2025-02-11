# pylint: disable=R1719
import json
from datetime import datetime

from collections import OrderedDict, Counter
# from mongo.mongo import search_for_article_by_pmid
from .journal_title_abbreviation import get_journal_title_abbreviation

from datetime import datetime

def datetime_converter(o):
    if isinstance(o, datetime):
        return o.isoformat()
    raise TypeError(f"Object of type {o.__class__.__name__} is not JSON serializable")


def get_min_max_year(data_list: dict):
    """Get min and max year of publcation from the documents found about the respective codename

    Args:
        data_list (dict): list of documents already filtered

    Returns:
        Returne just a dictonary containing max and min int number or None if data_list doesn't exist.
    """
    if isinstance(data_list, list):
        years_end_list = []
        for data in data_list:

            years = [
                year for year in data["chart"]["labels_year"] if year != "No date"
            ]  # don't use remove to avoid mutation

            if years:
                years_end_list.extend(years)

        if years_end_list:
            return {"min": min(years_end_list), "max": max(years_end_list)}

    return None


def display_function(processed_doc, show: str):
    """Filter data between:
        - TOTAL: all data found by the search
        - TP: True Positives
        - FP: False Positives
        - PUBCHEM: codename found on Pubchem
        - padlock: manual changes (releated the field validated_by_pipeline)

    Args:
        processed_doc: List of dictonary containing the processed data for all documents found
        show (str): type of filter to show (TOTAL/FP/TP/PUBCHEM)

    Returns:
        Return a dictonary contain the follow fields:
        - data_list: list of documents processed with information about the properties (use to pretty_print and charts)
        - total_found:
    """

    # Filter only True Positivies or False Positives
    if show in ["TP", "FP"]:
        boolean_type = True if show == "TP" else False
        data_list = [
            doc for doc in processed_doc["data_list"] if doc["TP"] is boolean_type
        ]

    # Filter only codenames found in PubChem
    if show == "PUBCHEM":
        data_list = [doc for doc in processed_doc["data_list"] if doc["in_pubchem"]]

    
    if show == "PADLOCK":
        data_list = [doc for doc in processed_doc["data_list"] if not doc["validated_by_pipeline"]]

    
    counter_field_TP = processed_doc["counter_field_TP"]
    total_chart = processed_doc["total_chart"]

    # P.S if show is not TP, FP or PUBCHEM that means it gonna return the TOTAL
    return {
        "data_list": data_list,
        "total_found": len(data_list),
        "counter_field_TP": counter_field_TP,
        "total_chart": total_chart
    }

class ObjTotalYearsJournals():
    
    def __init__(self):
        self.total_count_years = Counter()
        self.total_count_journals = Counter()
    
    def count(self, count_years, count_journals):

        
        self.total_count_years  += count_years
        self.total_count_journals += count_journals

    
def process_documents(documents: list):
    data_list = []
    counter_field_TP = count_TP_FP_pubchem(documents)

    if documents:
        
        # Count total Years and Journals
        total_years_journals = ObjTotalYearsJournals()
        
        for document in documents:
            if document:
                
                ###### Process Chart (Make a function after) #####
                year_journal = chart_bar_data(document)
                
                total_years_journals.count(
                    count_years=year_journal["years"],
                    count_journals=year_journal["journals"]
                )
                
                chart = {
                    "data_year": list(year_journal["years"].values()),
                    "labels_year": list(year_journal["years"].keys()),
                    "data_journal": list(year_journal["journals"].values()),
                    "labels_journal": list(year_journal["journals"].keys()),
                }
                ######################################################
                # Get the First article from article_list (article is in pubmedArticles_parsed)
                first_element_article = document["article_list"][0]
                
                # it's going to Jinja2
                data_list.append(
                    {
                        "chart": chart, # chart_bar_data(document),
                        "pretty_print_document": pretty_print_document(document),
                        "codename": document["codename"],
                        # "list_pmid":[doc["pmid"] for doc in document["article_list"] ],
                        "compound_id": document["compound_id"],
                        "pubmed_count_results": document["pubmed_count_results"]
                        if document.get("pubmed_count_results")
                        else None,
                        "TP": document["true_positive"],
                        "in_pubchem": document["in_pubchem"],
                        # "bing_search": document["bing_search"],
                        "possible_synonyms": document["possible_synonyms"]
                        if document.get("possible_synonyms")
                        else [],
                        "comment": document["comment"]
                        if document.get("comment")
                        else "",
                        "class": document["class"] if document.get("class") else "",
                        "validated_by_pipeline": document.get("validated_by_pipeline"),
                        "first_element_article":first_element_article
                    }
                )

        return {
            "data_list": data_list,
            "total_found": len(data_list),
            "counter_field_TP": counter_field_TP,
            "total_chart":process_total_chart_obj(total_years_journals)
        }

    return None

def process_total_chart_obj(obj):
    
    if obj:

        obj.total_count_years = dict(OrderedDict(sorted(obj.total_count_years.items())))
        obj.total_count_journals = dict(OrderedDict(sorted(obj.total_count_journals.items())))

        return{
            "data_year": list(obj.total_count_years.values()),
            "labels_year": list(obj.total_count_years.keys()),
            "data_journal": list(obj.total_count_journals.values()),
            "labels_journal": list(obj.total_count_journals.keys()),
        }
    
    return None

def count_TP_FP_pubchem(documents):
    """
    Return a number of True Positives, False Positives and codenames found on Pubchem
    """

    counter = Counter()

    for doc in documents:

        if doc["true_positive"]:
            counter["TP"] += 1
        else:
            counter["FP"] += 1

        if doc["in_pubchem"]:
            counter["in_pubchem"] += 1
        
        if not doc["validated_by_pipeline"]:
            counter["padlock"] += 1

    return {
        "TOTAL": counter["TP"] + counter["FP"],
        "TP": counter["TP"],
        "FP": counter["FP"],
        "in_pubchem": counter["in_pubchem"],
        # somecases the field validated by pipeline doesn't exist
        "padlock": counter["padlock"] if counter["padlock"] else 0
    }


def chart_bar_data(document: dict):
    """Organize the data for the Years & Journal Charts

    Args:
        document (dict): dict containing information about the codename

    Returns:
        Return a dict with labels (year & journal) and data year for the charts bar
    """

    years, journals = Counter(), Counter()

    for article in document["article_list"]:
        year = str(article["publication_date"].year) if article["publication_date"] is not None else "No date"
        journal = get_journal_title_abbreviation(str(article["journal"]))

        years[year] += 1
        journals[journal] += 1

    years = dict(OrderedDict(sorted(years.items())))
    journals = dict(OrderedDict(sorted(journals.items())))

    return {
        "years": years,
        "journals": journals
    }


def pretty_print_document(document: dict):
    """function to organize the data for the Pretty Print format in the HTML page.
    Example of the output: '{\n    "key_A": "value_A",\n    "key_B": "value_B"\n}'

    Args:
        document (dict): dict containing information about the codename.

    Returns:
        Return a string.
    """
    # convert the datetime object to string representation
    document["created"] = document["created"].isoformat() if isinstance( document["created"], datetime) else document["created"]
    document["last_update"] = document["last_update"].isoformat() if isinstance( document["last_update"], datetime) else document["last_update"]
    
    # Check if the codename was in the title and abstract of all papers
    # if ALL is True, big change to be a True Positive
    document["all_in_abstract_and_title"] = all(doc["in_abstract_and_title"] for doc in document["article_list"] )
    
    # Get Abstract and Title from the first element
    # document["random_article"] = search_for_article_by_pmid(document["article_list"][0]["pmid"]) if document.get("article_list") else None


    # Ordering -> String, Integer, Boolean, List
    desired_order_list = [
        "codename",
        "created",
        "last_update",
        "compound_id",
        "true_positive",
        "all_in_abstract_and_title", # I had to put "in_abstract_and_title" inside "article_list"
        "validated_by_pipeline",
        "in_pubchem",
        # "random_article",
        "article_list",
    ]
    reordered_dict = { k: document.get(k,None) for k in desired_order_list }  # if document.get(k)}
    
    return json.dumps(reordered_dict, indent=4, separators=(",", ": "), default=datetime_converter)
