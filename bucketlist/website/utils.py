import re


def normalize(query_string):
    """Returns a tuple of words from a query statement
    """
    findterms = re.compile(r'"([^"]+)"|(\S+)').findall(query_string)
    normspace = re.compile(r'\s{2,}').sub
    return (normspace(' ', (t[0] or t[1]).strip()) for t in findterms)
