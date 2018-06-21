import logging
import datetime
import re
import requests

from models.post import Post
from logger import logger


newegg_logger = logger.get_logger('Newegg', './logfile.log', logging.INFO)


def get_html(url: str):
    """
    Given a newegg URL, return raw HTML
    :param url: str, newegg url
    :return: str, html from url
    """
    headers = {
        'DNT': '1',
        'Host': 'www.newegg.com',
    }
    return requests.get(url, headers=headers).text


def get_mpn(html: str):
    """
    Given newegg html, return mpn
    :param html: str, raw html
    :return: str, mpn
    """
    pattern = "(?<=product_model:\[\\')(.*)(?=\\'\])"
    data = re.search(pattern, html)

    try:
        mpn = data.group(0)
    except AttributeError as e:
        newegg_logger.error(f'get_mpn: AttributeError: {e}')
        newegg_logger.error(f'data: {data}')
        return None
    else:
        return mpn


def get_price(html: str):
    """
    Given newegg html, return int price
    :param html: str, raw html
    :return: int, price, rounded
    """
    pattern = "(?<=product_sale_price:\[\\')(.*)(?=\\'\])"
    data = re.search(pattern, html)

    try:
        price = data.group(0)
    except AttributeError as e:
        newegg_logger.error(f'get_price: AttributeError: {e}')
        newegg_logger.error(f'data: {data}')
        return None

    try:
        price = int(round(float(price)))
    except ValueError as e:
        newegg_logger.error(f'get_price: ValueError: {e}')
        newegg_logger.error(f'price: {price}')
        return None

    return price


def ne_run(submission):
    """
    Given a submission, return a Post object
    :param submission: praw.Reddit.submission
    :return: Post
    """
    # TODO: add markdown
    url = submission.url

    html = get_html(url)

    mpn = get_mpn(html)
    price = get_price(html)

    post = Post(submission.fullname,
                mpn,
                price,
                datetime.date.today(),
                'newegg.com',
                )

    return post, None


def main():
    """
    url = 'https://www.newegg.com/Product/Product.aspx?Item=N82E16813128972&ignorebbr=1'
    post, markdown = ne_run(url)

    print(post)

    if markdown is None:
        print('md is none')
    else:
        print('md aint none')
    """
    pass


if __name__ == '__main__':
    main()


