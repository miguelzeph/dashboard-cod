# Check on mongo -> db.pubmedArticles.distinct("MedlineCitation.Article.Journal.Title")

journal_title_dict = {
    "ACS medicinal chemistry letters": "ACS M.C.Lett.",
    "Journal of medicinal chemistry": "J.M.Chem.",
    "British journal of pharmacology": "Br.J.Pharm.",
    "Bioorganic & medicinal chemistry":"Bioo.M.Chem",
    "Bioorganic & medicinal chemistry letters":"Bioo.M.Chem.Lett",
    "European journal of medicinal chemistry":"Eur.J.M.Chem",
}


def get_journal_title_abbreviation(journal_title: str):
    """Convert the journal full name to its own abbreveation.
    This converting was necessary due to the x-lable form the bar chart didn't suport the journal full name.

    Args:
        journal_title (str): original name provedied from DataScience.pubmedArticles collection.

    Returns:
        Return the journal abbreveation.
    """

    if journal_title in journal_title_dict:
        journal_title = journal_title_dict.get(journal_title)
    return journal_title
