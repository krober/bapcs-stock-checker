import re
import requests

from lxml import html

from stores.registration import register
from logger import logger


ebay_logger = logger.get_logger('Ebay', './logfile.log')


def get_page(url: str):
    return requests.get(url)


def get_xpath(path: str, tree: html.HtmlElement):
    try:
        element = tree.xpath(path)[0]
    except IndexError as e:
        # attribute doesnt exist = sale splash page/bad link/local pickup, etc
        ebay_logger.error(f'{e.__class__}: {path}: {e}')
        return None
    else:
        return element


def get_item_number(tree: html.HtmlElement):
    path = '//div[@id="descItemNumber"]/text()'
    number = get_xpath(path, tree)
    return number


def get_price(tree: html.HtmlElement):
    path = '//span[@id="prcIsum"]'
    price_tag = get_xpath(path, tree)
    if price_tag is not None:
        price = price_tag.get('content')
        price = int(round(float(price)))
        return price
    return None


def get_seller(tree: html.HtmlElement):
    path = '//a[@id="mbgLink"]'
    seller_tag = get_xpath(path, tree)
    if seller_tag is not None:
        seller = seller_tag.get('aria-label')
        seller = seller.split(u'\xa0')[-1]
        return seller
    return None


def get_feedback(text: str):
    pattern = '(?s)(?<=feedback score: )(.*?)(?=")'
    data = re.search(pattern, text)
    try:
        feedback = data.group(0).strip()
    except AttributeError as e:
        # No itemprop="mpn" found = mpn not entered by seller
        ebay_logger.error(f'{e.__class__}: {e}')
        return None
    else:
        feedback = int(feedback)
        return feedback


def get_score(tree: html.HtmlElement):
    path = '//div[@id="si-fb"]/text()'
    score = get_xpath(path, tree)
    if score is not None:
        score = score.split(u'\xa0')[0]
    return score


def get_mpn(text: str):
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
    Given a submission, return a Post object
    :param submission: praw.Reddit.submission
    :return: Post
    """
    # TODO: add markdown
    page = get_page(submission.url)
    content = page.content
    text = page.text
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
    # content = page.content
    # text = page.text
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







