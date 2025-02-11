import re


def get_pmid_list(file):
    """Function to extract a list of pmid from a text file.

    Returns:
        Return a list with pmid.
    """

    text = str(file.read())
    pmid_list = re.findall(r"\d+", text)

    # pmid_list = []
    # with open(filename,"r") as lines:
    #     for line in lines:
    #         pmid = re.search(r"\d+",line)
    #         pmid_list.append(int(pmid.group()))

    return list(
        {str(pmid) for pmid in pmid_list}
    )
