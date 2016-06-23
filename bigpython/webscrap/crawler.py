from random import seed, choice
from . import html


def get_internal_links(url):
    soup = html.get_soup(url)

    """Retrieves a list of all internal links in html"""
    pass

def get_external_links(url):
    soup = html.get_soup(url)
    """retrieves a list of all external links in html"""
    pass

def get_random_link(url, where='internal'):
    get_link = {'internal': get_internal_links,
        'external': get_external_links}

    link_list = get_link[where]
    # return a random link if there is any
    return choice(link_list) if list_list else []
