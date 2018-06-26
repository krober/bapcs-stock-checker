import re
import requests

from lxml import html

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
        element = tree.xpath(path)[0]
    except IndexError as e:
        # Combo deals/splash pages/etc
        amazon_logger.error(f'{e.__class__}: {path}: {e}')
        return None
    else:
        return element


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
    path = '//span[@id="priceblock_ourprice"]'
    price_tag = get_xpath(path, tree)
    if price_tag is not None:
        price = price_tag.text[1:]
        price = int(round(float(price)))
        return price
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

    # url = 'https://www.amazon.com/Crucial-MX500-NAND-SATA-Internal/dp/B077SF8KMG'
    # url = 'https://www.amazon.com/RIPJAWS-KM570-Cherry-Speed-Silver/dp/B01LZEVDKI/'
    # url = 'https://www.amazon.com/Kingston-120GB-Solid-SA400S37-120G/dp/B01N6JQS8C/ref=mp_s_a_1_6?ie=UTF8&qid=1528906162&sr=8-6&pi=AC_SX236_SY340_QL65&keywords=ssd&dpPl=1&dpID=41EjY-AhQUL&ref=plSrch'
    # url = 'https://www.amazon.com/TP-Link-RangeBoost-Technology-Archer-A2300/dp/B0751RK6XZ/ref=sr_1_1?m=A3C0IBSA2XBL9N&s=merchant-items&ie=UTF8&qid=1528439208&sr=1-1&refinements=p_4%3ATP-Link&dpID=51LmWDKvBnL&preST=_SX300_QL70_&dpSrc=srch'
    # url = 'https://www.amazon.com/Inland-Professional-480GB-Internal-Solid/dp/B07BD32RLK'
    #
    # page = get_page(url)
    # text = page.text
    # content = page.content
    # tree = html.fromstring(content)
    #
    # price = get_price(tree)
    # mpn = get_mpn(text)
    #
    # print(price)
    # print(mpn)

    pass


if __name__ == '__main__':
    main()


















