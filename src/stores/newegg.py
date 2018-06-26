import re
import requests

from stores.registration import register
from logger import logger


newegg_logger = logger.get_logger('Newegg', './logfile.log')


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
    page = get_page(submission.url)
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

    # url = 'https://www.newegg.com/Product/Product.aspx?Item=N82E16813128972&ignorebbr=1'
    # url = 'https://www.amazon.com/Crucial-MX500-NAND-SATA-Internal/dp/B077SF8KMG'
    # url = 'https://www.amazon.com/RIPJAWS-KM570-Cherry-Speed-Silver/dp/B01LZEVDKI/'
    # url = 'https://www.amazon.com/Kingston-120GB-Solid-SA400S37-120G/dp/B01N6JQS8C/ref=mp_s_a_1_6?ie=UTF8&qid=1528906162&sr=8-6&pi=AC_SX236_SY340_QL65&keywords=ssd&dpPl=1&dpID=41EjY-AhQUL&ref=plSrch'
    # url = 'https://www.amazon.com/TP-Link-RangeBoost-Technology-Archer-A2300/dp/B0751RK6XZ/ref=sr_1_1?m=A3C0IBSA2XBL9N&s=merchant-items&ie=UTF8&qid=1528439208&sr=1-1&refinements=p_4%3ATP-Link&dpID=51LmWDKvBnL&preST=_SX300_QL70_&dpSrc=srch'
    #
    # page = get_page(url)
    # text = page.text
    #
    # price = get_price(text)
    # mpn = get_mpn(text)
    #
    # print(price)
    # print(mpn)

    pass


if __name__ == '__main__':
    main()


