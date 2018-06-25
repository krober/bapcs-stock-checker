import requests

from stores.registration import register
from logger import logger

# TODO change 'store_name' to name of store being parsed
store_name_logger = logger.get_logger('Store_name', './logfile.log')


"""
The below functions are just suggestions, they do not have to be 
implemented in exactly this manner, or at all
"""


def get_html(url: str):
    # do something
    pass


def extract_from_html(pattern: str, html: str):
    # do something
    pass


def get_mpn(html: str):
    # do something
    pass


def get_price(html: str):
    # do something
    pass


"""
This one is required, but the name can be anything
Decorator should include friendly domain name, as it is what 
urls will be checked against when determining which
store parser to use. ex. 'newegg.com'.  Decorator and import
may be removed/commented out to run this module independently
"""


@register('your-store.com')
def ne_run(submission):
    """
    Given a submission, return a dictionary containing
    the mpn and price (either may be None), and optionally
    a markdown formatted string (also may be None) to be used as
    a reddit comment.  Due to a wide variety of factors,
    such as network errors, sites being down, excess traffic
    to sites, etc, the mpn & price dictionary and the markdown
    string may be returned as None.  The submission's fullname
    will still be saved to the database as having been 'parsed'.
    :param submission: praw.Reddit.submission
    :return: dict, str; product_details and markdown
    """

    # again, just a template
    url = submission.url
    html = get_html(url)

    mpn = get_mpn(html)
    price = get_price(html)

    product_details = {
        'mpn': mpn,
        'price': price,
    }

    markdown = None

    return product_details, markdown


def main():
    pass


if __name__ == '__main__':
    main()


