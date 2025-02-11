# pylint: disable=E0602
from datetime import datetime
from klein_mongo import get_client
from klein_config import get_config

config = get_config()

# Database
client = get_client(config)
db = client[config.get("mongo.database")]

# Collection
# collection_articles_parsed = db[config.get("mongo.collection_articles_parsed")]
collection_articles_codename = db[config.get("mongo.collection_articles_codename")]

# Functions

# def search_for_article_by_pmid(pmid: int):
#     """Use a pmid to search for articles in the pubmedArticles collection.

#     Args:
#         pmid (int)

#     Returns:
#         Return a dict {"pmid":...,"title":..., "abstract":...}
#     """

#     article =  collection_articles_parsed.find_one({"pmid":pmid})
#     if article:
#         return {
#             "pmid":article.get("pmid"),
#             "abstract": article.get("abstract_parsed").get("abstract") if article.get("abstract_parsed") else None,
#             "title": article.get("title_parsed").get("title") if article.get("title_parsed") else None,
#             # "year": article["year_publication"]
#         }
        
#     return None

def get_blacklist_FP():
    """List all False Positives codename as a blacklist

    Returns:
        List contaning false codenames
    """

    curs = collection_articles_codename.aggregate(
        [
            {"$match": {"true_positive": False}},
            {"$project": {"_id": 0, "codename": 1}},
        ]
    )

    return [obj["codename"] for obj in curs]


def search_for_pmid(pmid_list: list):
    """Use a list contaning pmid to search for articles in the pubmedArticles collection.

    Args:
        pmid_list (list): list of pmid (int).

    Returns:
        Return a list of documents found by the respective pmid.
    """

    # This way you will avoid obj repetition in the list
    return list(
        collection_articles_codename.find({"article_list.pmid": {"$in": pmid_list}})
    )
    
def search_for_drug_name_list(drug_name_list: list):
    """Use a list contaning pmid to search for articles in the pubmedArticles collection.

    Args:
        drug_name_list (list): list of drug name.

    Returns:
        Return a list of documents found by the respective drug name.
    """
    
    # This way you will avoid obj repetition in the list
    return list(
        collection_articles_codename.find({"codename": {"$in": drug_name_list}})
    )


def search_for_drug_name(drug_name: str):
    """Use a list contaning pmid to search for articles in the pubmedArticles collection.

    Try to find the name exactly. If not found anything, try yo make a case-isensitive query (similar ILIKE from postgresql )

    Args:
        drug_name (str): drug name or codename for search in the pubmedArticles_synonyms_blacklist.

    Returns:
        Return a list of documents found by the respective drug_name/codename.
    """

    # Find Exactly
    curs = list(
        collection_articles_codename.aggregate(
            [{"$match": {"codename": {"$regex": fr"^{drug_name}$", "$options": "i"}}}]
        )
    )

    # Find similar if not found the codename
    if not curs:
        curs = list(
            collection_articles_codename.aggregate(
                [{"$match": {"codename": {"$regex": fr"{drug_name}", "$options": "i"}}}]
            )
        )

    return curs


def search_for_drug_name_regex(regex: str):

    curs = list(
        collection_articles_codename.aggregate([
            {'$match': {'codename': {"$regex": fr"^{regex}$", "$options": "i"}}},
            {'$group': {
                '_id': None, 
                'TP': {
                    '$sum': {
                        '$cond': [{'$eq': ['$true_positive', True]}, 1, 0]
                    }
                }, 
                'FP': {
                    '$sum': {
                        '$cond': [{'$eq': ['$true_positive', False]}, 1, 0]
                    }
                }
                }
            },
            {'$project': {
                '_id': 0, 
                'TP': 1, 
                'FP': 1,
                'total': {
                    '$add': ['$TP', '$FP']
                }, 
                'regex': str(regex)
                }
            }
            ]
        )
    )
    
    if curs:
    
        return curs[0]
    
    return {"regex":regex}
    


def updating_codename(obj):
    """Saving obj into collection"""

    # Update
    collection_articles_codename.update_one(
        {  # Filter
            "codename": obj["codename"],
            # "true_positive": obj["true_positive"]
            # If doesn't exist create... if exist update.
            # P.S Always filter by "pmid" instead of "_id" because this "_id"
            # is from pubmedAbstracts and some documents from pubmedAbstract_Synonyms has different one from there.
        },
        {
            "$set": {
                "true_positive": obj["true_positive"],
                "comment": obj["comment"],
                "class": obj["class"],
                "validated_by_pipeline": obj["validated_by_pipeline"],
                "last_update": datetime.today(),
            }
            #
        },
        upsert=True,
    )

def get_data_report_general():
    
    pipeline = [
        {
            '$project': {
                "_id":0,
                'codename': 1, 
                # 'article_list.journal': 1, 
                # 'article_list.year': 1, 
                # 'article_list.in_abstract_and_title': 1, 
                'in_pubchem': 1, 
                'true_positive': 1, 
                'validated_by_pipeline': 1, 
                'pubmed_count_results': 1, 
                'created': { "$substr": [ { "$dateToString": { "date": "$created" } }, 0, 10 ] }, 
                # 'last_update': { "$substr": [ { "$dateToString": { "date": "$last_update" } }, 0, 10 ] }, 
            }
        },
        {'$sort': {'created': -1}}
    ]
    
    data = collection_articles_codename.aggregate(pipeline)

    return list(data)

def get_data_report_count_codename(
    true_positive:bool=True,
    sort_count:int=-1):
    
    pipeline = [
        {"$match":{"true_positive":{"$eq":true_positive}}},
        {"$unwind": "$article_list"},
        {"$group": {"_id": "$codename", "count": {"$sum": 1}}},
        {"$project":{"codename":"$_id","count":1}},
        {"$sort": {"count":sort_count}},
        # {"$limit": 100},
    ]
    
    data = collection_articles_codename.aggregate(pipeline)

    return list(data)