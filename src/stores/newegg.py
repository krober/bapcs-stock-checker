import re

import requests

from logger import logger
from stores.registration import register


newegg_logger = logger.get_logger('Newegg', './logfile.log')


def convert_mobile_url(url: str):
    """
    Check for m.newegg.com...
    :param url: str, mobile newegg url
    :return: str, non-mobile link
    """
    if 'm.newegg.com' in url:
        base_url = 'https://www.newegg.com/Product/Product.aspx?Item='
        pattern = '(?s)(?<=products/)(.*?)(?=\?)'
        item = re.search(pattern, url)
        try:
            item = item.group(0).strip()
        except AttributeError as e:
            newegg_logger.error(f'{e.__class__}: {e}')
            return None
        else:
            url = base_url + item
    return url


def get_page(url: str):
    """Simple request based on url"""
    headers = {
        'DNT': '1',
        'Host': 'www.newegg.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
    }
    return requests.get(url, headers=headers)


def extract_from_text(pattern: str, text: str):
    """
    Given newegg text, return item matching pattern
    :param pattern: str, pattern to search against
    :param text: str, requests.get().text to search
    :return: str, found data or None if not found/exception
    """
    data = re.search(pattern, text)
    try:
        data = data.group(0)
    except AttributeError as e:
        # usually combo deals, also flash.newegg.com
        newegg_logger.error(f'{e.__class__}: {pattern}: {e}')
        return None
    else:
        return data


def get_mpn(text: str):
    """
    Given newegg text, return mpn
    :param text: str, requests.get().text to search
    :return: str, mpn
    """
    pattern = "(?<=product_model:\[\\')(.*)(?=\\'\])"
    mpn = extract_from_text(pattern, text)
    return mpn


def get_price(text: str):
    """
    Given newegg text, return int price
    :param text: str, requests.get().text to search
    :return: int, price, rounded; None if unable to cast
    """
    pattern = "(?<=product_sale_price:\[\\')(.*)(?=\\'\])"
    price_text = extract_from_text(pattern, text)
    try:
        price = int(round(float(price_text)))
    except ValueError as e:
        # usually 'see price in cart' deals
        newegg_logger.error(f'{e.__class__}: {pattern}: {e}')
        return None
    except TypeError as e:
        newegg_logger.error(f'{e.__class__}: {pattern}: {e}')
        return None
    else:
        return price


@register('newegg.com')
def ne_run(submission):
    """
    Given a submission, return product details
    :param submission: praw.Reddit.submission
    :return: dict, product_details
    """
    # TODO: add markdown
    url = convert_mobile_url(submission.url)

    if url is None:
        return None, None

    page = get_page(url)
    text = page.text

    mpn = get_mpn(text)
    price = get_price(text)

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

