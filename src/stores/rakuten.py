import re
import requests

from stores.registration import register
from logger import logger


rakuten_logger = logger.get_logger('Rakuten', './logfile.log')


def get_page(url: str):
    """Simple request based on url"""
    headers = {
        'DNT': '1',
        'Host': 'www.rakuten.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
    }
    return requests.get(url, headers=headers)


def get_price(text: str):
    """
    Parses for price
    :param text: str, from requests.get().text
    :return: int, rounded, if exists; else None
    """
    pattern = '(?<="price" content=")(.*?)(?="/>)'
    data = re.search(pattern, text)
    try:
        data = data.group(0).strip()
    except AttributeError as e:
        # Combo deals/splash pages/etc
        rakuten_logger.error(f'{e.__class__}: {e})')
        return None
    try:
        price = int(round(float(data)))
    except TypeError as e:
        # Combo deals/splash pages/etc
        rakuten_logger.error(f'{e.__class__}: {e})')
        return None
    else:
        return price


def get_mpn(text: str):
    """
    Parses for price
    :param text: str, from requests.get().text
    :return: int, rounded, if exists; else None
    """
    pattern = '(?<=MPN</th><td>)(.*?)(?=</td>)'
    data = re.search(pattern, text)
    try:
        mpn = data.group(0).strip()
    except AttributeError as e:
        # Combo deals/splash pages/mailers/etc
        rakuten_logger.error(f'{e.__class__}: {e})')
        return None
    else:
        return mpn


@register('rakuten.com')
def ra_run(submission):
    """
    Given a submission, return product details
    :param submission: praw.Reddit.submission
    :return: dict, product_details
    """
    # TODO: add markdown
    page = get_page(submission.url)
    text = page.text

    price = get_price(text)
    mpn = get_mpn(text)

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

