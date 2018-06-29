import re

from lxml import html
import requests

from stores.registration import register
from logger import logger


amazon_logger = logger.get_logger('Amazon', './logfile.log')


def get_page(url: str):
    """Simple request based on url"""
    headers = {
        'DNT': '1',
        'Host': 'www.amazon.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
    }
    return requests.get(url, headers=headers)


def get_xpath(path: str, tree: html.HtmlElement):
    """
    Looks for path/element in tree
    :param path: str, valid xpath search string
    :param tree: html.HtmlElement from lxml
    :return: element, based on path; or None if not found
    """
    try:
        return tree.xpath(path)[0]
    except IndexError:
        # Combo deals/splash pages/etc
        raise IndexError


def extract_from_text(pattern: str, text: str):
    """
    Given requests.get().text, extract based on pattern
    :param pattern: str, pattern to search against
    :param text: str, requests.get().text to search
    :return: str, found data or None if not found/exception
    """
    data = re.search(pattern, text)
    try:
        data = data.group(0).strip()
    except AttributeError as e:
        # Combo deals/splash pages/etc
        amazon_logger.error(f'{e.__class__}: {pattern}: {e}')
        return None
    else:
        return data


def get_price(tree: html.HtmlElement):
    """
    Parses price from amazon page
    :param tree: html.HtmlElement from lxml
    :return: int, rounded, if exists; else None
    """
    paths = [
        '//span[@id="priceblock_ourprice"]',
        '//span[@id="priceblock_dealprice"]',
    ]
    for path in paths:
        try:
            price_tag = get_xpath(path, tree)
        except IndexError as e:
            amazon_logger.error(f'{e.__class__}: {path}: {e}')
            continue
        else:
            break
    try:
        return int(round(float(price_tag.text[1:])))
    except UnboundLocalError as e:
        amazon_logger.error(f'{e.__class__}: {e}')
        return None
    except TypeError as e:
        amazon_logger.error(f'{e.__class__}: {price_tag.text}: {e}')
        return None


def get_mpn(text: str):
    """
    Parses mpn for product
    :param text: str, from requests.get().text
    :return: str, manuf. product number, if
    entered by seller; else None
    """
    parent_pattern = '(?s)(?<=Item model number)(.*?)(?=/td>)'
    parent_tag = extract_from_text(parent_pattern, text)
    if parent_tag is not None:
        mpn_pattern = '(?s)(?<=base">)(.*?)(?=<)'
        mpn = extract_from_text(mpn_pattern, parent_tag)
        return mpn
    return None


@register('amazon.com')
def am_run(submission):
    """
    Given a submission, return product details
    :param submission: praw.Reddit.submission
    :return: dict, product_details
    """
    # TODO: add markdown
    page = get_page(submission.url)
    text = page.text
    content = page.content
    tree = html.fromstring(content)

    mpn = get_mpn(text)
    price = get_price(tree)

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

