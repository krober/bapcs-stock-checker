import logging
import datetime
import requests

from stores.registration import register
from logger import logger
from models.post import Post

# TODO change store_name to name of store being parsed
store_name_logger = logger.get_logger('Store_name', './logfile.log', logging.INFO)


"""
The below functions are just suggestions, they do not have to be implemented in 
exactly this manner, or at all
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
store parser to use. ex. 'newegg.com'
"""


@register('your_store.com')
def ne_run(submission):
    """
    Given a submission, return a Post object and optionally
    a markdown formatted string to be used as reddit comment
    Either may be None, but strongly recommend at least creating
    a Post object with submission.fullname
    :param submission: praw.Reddit.submission
    :return: Post, str; Post object and markdown
    """

    # again, just a template
    url = submission.url
    html = get_html(url)

    mpn = get_mpn(html)
    price = get_price(html)

    post = Post(submission.fullname,
                mpn,
                price,
                datetime.date.today(),
                'your_store.com',
                )

    return post, None


def main():
    pass


if __name__ == '__main__':
    main()


