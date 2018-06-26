import re
import requests

from lxml import html

from stores.registration import register
from logger import logger


bestbuy_logger = logger.get_logger('BestBuy', './logfile.log')


def get_page(url: str):
    """Simple request based on url"""
    headers = {
        'DNT': '1',
        'Host': 'www.bestbuy.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
    }
    return requests.get(url, headers=headers)


def get_price(text: str):
    """
    Parses for price
    :param text: str, from requests.get().text
    :return: int, rounded, if exists; else None
    """
    pattern = '(?<=customerPrice":)(.*?)(?=,)'
    data = re.search(pattern, text)
    try:
        data = data.group(0).strip()
    except AttributeError as e:
        # Combo deals/splash pages/etc
        bestbuy_logger.error(f'{e.__class__}: {e})')
        return None
    try:
        price = int(round(float(data)))
    except TypeError as e:
        # Combo deals/splash pages/etc
        bestbuy_logger.error(f'{e.__class__}: {e})')
        return None
    else:
        return price


def get_mpn(tree: html.HtmlElement):
    """
    Parses mpn from bestbuy page
    :param tree: html.HtmlElement from lxml
    :return: str, manuf. product number, if exists; else None
    """
    path = '//span[@id="model-value"]'
    try:
        mpn_tag = tree.xpath(path)[0]
    except IndexError as e:
        # Combo deals/splash pages/etc
        bestbuy_logger.error(f'{e.__class__}: {e}')
        return None
    else:
        return mpn_tag.text


@register('bestbuy.com')
def bb_run(submission):
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

    price = get_price(text)
    mpn = get_mpn(tree)

    product_details = {
        'mpn': mpn,
        'price': price,
    }

    markdown = None

    return product_details, markdown


def main():

    # url = ''
    # url = 'https://www.bestbuy.com/site/searchpage.jsp?id=pcat17071&st=logitech+g'
    # url = 'https://www.bestbuy.com/site/dell-27-led-qhd-gsync-monitor-black/5293502.p?skuId=5293502'
    # url = 'https://www.bestbuy.com/site/hp-omen-by-hp-desktop-intel-core-i5-8gb-memory-nvidia-geforce-gtx-1060-1tb-hard-drive-brushed-aluminum/5759916.p?skuId=5759916'
    # url = 'https://www.bestbuy.com/site/cyberpowerpc-gamer-ultra-vr-desktop-amd-ryzen-7-series-16gb-memory-nvidia-geforce-gtx-1070-120gb-solid-state-drive-1tb-hdd-black/6092500.p'
    #
    # page = get_page(url)
    # text = page.text
    # content = page.content
    # tree = html.fromstring(content)
    #
    # price = get_price(text)
    # mpn = get_mpn(tree)
    #
    # print(url)
    # print(price)
    # print(mpn)

    pass


if __name__ == '__main__':
    main()


















