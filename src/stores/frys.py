import requests

from lxml import etree, html

from stores.registration import register
from logger import logger


frys_logger = logger.get_logger('Frys', './logfile.log')


def get_page(url: str):
    """Simple request based on url"""
    headers = {
        'DNT': '1',
        'Host': 'www.frys.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
    }
    return requests.get(url, headers=headers)


def get_price(tree: html.HtmlElement):
    """
    Parses price from page
    :param tree: html.HtmlElement from lxml
    :return: int, rounded, if exists; else None
    """
    path = '//span[@id="did_price1valuediv"]'
    try:
        price_tag = tree.xpath(path)[0].text
        price = int(round(float(price_tag[1:])))
    except IndexError as e:
        # Combo deals/splash pages/etc
        frys_logger.error(f'{e.__class__}: {e}')
        return None
    except TypeError as e:
        frys_logger.error(f'{e.__class__}: {e}')
        return None
    else:
        return price


def get_mpn(tree: html.HtmlElement):
    """
    Parses mpn from page
    :param tree: html.HtmlElement from lxml
    :return: str, manuf. product number, if exists; else None
    """
    path = '//span[@class="product-label-value"]'
    try:
        mpn_tag = tree.xpath(path)[1]
    except IndexError as e:
        # Combo deals/splash pages/etc
        frys_logger.error(f'{e.__class__}: {e}')
        return None
    else:
        return mpn_tag.text.strip()


@register('frys.com')
def fr_run(submission):
    """
    Given a submission, return product details
    :param submission: praw.Reddit.submission
    :return: dict, product_details
    """
    # TODO: add markdown
    page = get_page(submission.url)
    content = page.content

    try:
        tree = html.fromstring(content)
    except etree.ParserError as e:
        # Frys mailer/multiproduct links
        frys_logger.error(f'{e.__class__}: {e}')
        return None, None

    price = get_price(tree)
    mpn = get_mpn(tree)

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

