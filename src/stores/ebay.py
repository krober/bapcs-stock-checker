import re
import requests

from lxml import html

from stores.registration import register
from logger import logger


ebay_logger = logger.get_logger('Ebay', './logfile.log')


def get_page(url: str):
    """Simple request based on url"""
    headers = {
        'DNT': '1',
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
        # attribute doesnt exist = sale splash page/bad link/local pickup, etc
        ebay_logger.error(f'{e.__class__}: {path}: {e}')
        return None
    else:
        return element


def get_item_number(tree: html.HtmlElement):
    """Returns ebay item number"""
    path = '//div[@id="descItemNumber"]'
    number_tag = get_xpath(path, tree)
    if number_tag is not None:
        number = number_tag.text
        return number
    return None


def get_price(tree: html.HtmlElement):
    """
    Parses price from ebay page
    :param tree: html.HtmlElement from lxml
    :return: int, rounded, if exists; else None
    """
    path = '//span[@id="prcIsum"]'
    price_tag = get_xpath(path, tree)
    if price_tag is not None:
        price = price_tag.get('content')
        price = int(round(float(price)))
        return price
    return None


def get_seller(tree: html.HtmlElement):
    """
    Parses ebay seller name from ebay page
    :param tree: html.HtmlElement from lxml
    :return: str, seller name if exists; else None
    """
    path = '//a[@id="mbgLink"]'
    seller_tag = get_xpath(path, tree)
    if seller_tag is not None:
        seller = seller_tag.get('aria-label')
        seller = seller.split(u'\xa0')[-1]
        return seller
    return None


def get_feedback(text: str):
    """
    Parses total feedback count from ebay page
    :param text: str, from requests.get().text
    :return: int, total feedback for seller (stars); None if not available
    """
    pattern = '(?s)(?<=feedback score: )(.*?)(?=")'
    data = re.search(pattern, text)
    try:
        feedback = data.group(0).strip()
    except AttributeError as e:
        # Bad link, etc
        ebay_logger.error(f'{e.__class__}: {e}')
        return None
    else:
        feedback = int(feedback)
        return feedback


def get_score(tree: html.HtmlElement):
    """
    Parses % feedback score for seller
    :param tree: html.HtmlElement from lxml
    :return: str, ex '99.2%' - feedback score; None if not available
    """
    path = '//div[@id="si-fb"]'
    score_tag = get_xpath(path, tree)
    if score_tag is not None:
        score = score_tag.text
        score = score.split(u'\xa0')[0]
        return score
    return None


def get_mpn(text: str):
    """
    Parses mpn for product
    :param text: str, from requests.get().text
    :return: str, manuf. product number, if
    entered by seller; else None
    """
    pattern = '(?s)(?<=itemprop="mpn">)(.*?)(?=<)'
    data = re.search(pattern, text)
    try:
        mpn = data.group(0).strip()
    except AttributeError as e:
        # No itemprop="mpn" found = not entered by seller
        ebay_logger.error(f'{e.__class__}: {e}')
        return None
    else:
        return mpn


def is_free_shipping(tree: html.HtmlElement):
    """
    Determines if product offers free shipping
    :param tree: html.HtmlElement from lxml
    :return: True if free, else False; None if not found
    """
    path = '//span[@id="fshippingCost"]'
    ship_parent = get_xpath(path, tree)
    if ship_parent is not None:
        ship_child = ship_parent.getchildren()[0]
        ship_text = ship_child.text
        return ship_text == 'FREE'
    return None


@register('ebay.com')
def eb_run(submission):
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

    # item_number = get_item_number(tree)
    mpn = get_mpn(text)
    price = get_price(tree)
    # seller = get_seller(tree)
    # seller_feedback = get_feedback(text)
    # seller_score = get_score(tree)
    # free_shipping = is_free_shipping(tree)

    product_details = {
        'mpn': mpn,
        'price': price,
    }

    markdown = None

    return product_details, markdown


def main():

    # url = 'https://www.ebay.com/itm/NEW-AMD-RYZEN-7-2700X-8-Core-3-7-GHz-Socket-AM4-105W-YD270XBGAFBOX-Processor/273199602622'
    # url = 'https://www.ebay.com/itm/Best-Buy-Gift-Card-25-50-100-or-150-Fast-Email-delivery/262075905712?var=560853814071&_trkparms=%26rpp_cid%3D5b2894c84de66764007d7240%26rpp_icid%3D56ec4a8ce4b00bcc855a5463'
    # url = 'https://www.ebay.com/itm/Landmann-City-Lights-Memphis-Fire-Pit-Black-/182641297525'
    # url = 'https://pages.ebay.com/promo/2018/0621/66698.html?_trkparms=%26clkid%3D4767729480946058037'
    #
    # page = get_page(url)
    # text = page.text
    # content = page.content
    # tree = html.fromstring(content)
    #
    # item_number = get_item_number(tree)
    # price = get_price(tree)
    # seller = get_seller(tree)
    # seller_feedback = get_feedback(text)
    # seller_score = get_score(tree)
    # mpn = get_mpn(text)
    # free_shipping = is_free_shipping(tree)
    #
    # print(item_number)
    # print(price)
    # print(seller)
    # print(seller_feedback)
    # print(seller_score)
    # print(mpn)
    # print(free_shipping)

    pass


if __name__ == '__main__':
    main()







