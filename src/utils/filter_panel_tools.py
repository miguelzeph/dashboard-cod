# pylint: disable=R1719
def filter_documents(documents: dict, checkbox, slider_vals):
    if not checkbox:
        return None

    true_positive_values, in_pubchem_values = process_checkbox(checkbox)
    filter_1 = filter_true_positive(documents, true_positive_values)
    filter_2 = filter_in_pubchem(filter_1, in_pubchem_values)

    if not slider_vals:
        return filter_2

    return filter_by_year(filter_2, slider_vals)


def process_checkbox(checkbox):
    true_positive_values = []
    in_pubchem_values = []

    for value in checkbox:
        if value == "TP":
            true_positive_values.append(True)
        if value == "FP":
            true_positive_values.append(False)
        if value == "PUBCHEM":
            in_pubchem_values.append(True)
        if value == "NO_PUBCHEM":
            in_pubchem_values.extend([False, None])

    return true_positive_values, in_pubchem_values


def filter_true_positive(documents, true_positive_values):
    filter_1 = []

    for doc in documents:
        if doc["true_positive"] in true_positive_values:
            filter_1.append(doc)

    return filter_1


def filter_in_pubchem(documents, in_pubchem_values):
    filter_2 = []

    for doc in documents:
        if doc["in_pubchem"] in in_pubchem_values:
            filter_2.append(doc)

    return filter_2


def filter_by_year(documents, slider_vals):
    filter_3 = []

    
    for doc in documents:
        
        
        for article_info in doc.get("article_list", []):
            if not article_info:
                continue
            
            # Create field Year
            article_info["year"] = int(article_info["publication_date"].year)
            
            article_year = article_info["year"]
            
            if not article_year:
                continue
            if slider_vals["min"] <= article_year <= slider_vals["max"]:
                filter_3.append(doc)
                break

    return filter_3
