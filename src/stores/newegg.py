import logging
import datetime
import re
import requests

from stores.registration import register
from logger import logger
from models.post import Post


newegg_logger = logger.get_logger('Newegg', './logfile.log')


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


def extract_from_html(pattern: str, html: str):
    """
    Given newegg html, return item matching pattern
    :param pattern: str, pattern to search against
    :param html: str, html to search
    :return: str, found data or None if not found/exception
    """
    data = re.search(pattern, html)
    try:
        data = data.group(0)
    except AttributeError as e:
        newegg_logger.error(f'{e.__class__}: {pattern}: {e}')
        newegg_logger.error(f'data: {data}')
        return None
    else:
        return data


def get_mpn(html: str):
    """
    Given newegg html, return mpn
    :param html: str, raw html
    :return: str, mpn
    """
    pattern = "(?<=product_model:\[\\')(.*)(?=\\'\])"
    mpn = extract_from_html(pattern, html)
    return mpn


def get_price(html: str):
    """
    Given newegg html, return int price
    :param html: str, raw html
    :return: int, price, rounded; None if unable to cast
    """
    pattern = "(?<=product_sale_price:\[\\')(.*)(?=\\'\])"
    price_text = extract_from_html(pattern, html)
    try:
        price = int(round(float(price_text)))
    except ValueError as e:
        newegg_logger.error(f'{e.__class__}: {e}')
        newegg_logger.error(f'price_text: {price_text}')
        return None
    except TypeError as e:
        newegg_logger.error(f'{e.__class__}: {e}')
        newegg_logger.error(f'price_text: {price_text}')
        return None
    else:
        return price


@register('newegg.com')
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


