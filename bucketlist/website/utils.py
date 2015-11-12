from django.core.urlresolvers import reverse
import re


def get_http_referer(request, url):
    """Returns the URL from which a user was referred
    """
    name, id = url.split(':')
    long_url = reverse(default, kwargs={'id': id})
    referer = request.META.get('HTTP_REFERER')
    
    if not referer:
        return long_url

    # remove the protocol and split the url at the slashes
    referer = re.sub('^https?:\/\/', '', referer).split('/')
    if referer[0] != request.META.get('SERVER_NAME'):
        return long_url

    # add the slash at the relative path's view and finished
    referer = u'/' + u'/'.join(referer[1:])
    return referer

def normalize(query_string):
    """Returns a tuple of words from a query statement
    """
    findterms=re.compile(r'"([^"]+)"|(\S+)').findall(query_string)
    normspace = re.compile(r'\s{2,}').sub
    return (normspace(' ', (t[0] or t[1]).strip())  for t in findterms)