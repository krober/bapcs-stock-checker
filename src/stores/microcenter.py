import logging
import datetime
import json
import re
import requests

from stores.registration import register
from templates import mc_template
from logger import logger
from models.post import Post


mc_logger = logger.get_logger('Microcenter', './logfile.log', logging.INFO)


def strip_url(url: str):
    """
    Given a Microcenter URL, if query string is present, strip it and return
    stripped string.  Titles of products should not contain '?'
    :param url: str, microcenter url
    :return: str, stripped of query string as necessary
    """
    url = url[:url.find('?')]
    mc_logger.info(f'url: {url}')
    return url


def get_html(url: str, store_num: str='095'):
    """
    Given a Microcenter URL, return raw HTML
    :param url: str, microcenter url
    :param store_num: str, store number as string, defaults to MO - Brentwood
    :return: str, html from url
    """
    headers = {
        'Cookie': 'storeSelected=' + store_num,
        'DNT': '1',
        'Host': 'www.microcenter.com',
    }
    return requests.get(url, headers=headers).text


def extract_to_json(pattern: str, html: str):
    """
    Given raw Microcenter HTML and search pattern, find, format, and return matching python dictionary
    :param pattern: str, regex to search for in html
    :param html: str, raw html
    :return: dict, from html based on pattern
    """
    data = re.search(pattern, html)
    data_json = data.group(0)\
                    .strip()\
                    .replace("'", "\"")
    return json.loads(data_json)


def get_stores(html: str):
    """
    given mc html, return list stores
    :param html: str, raw html
    :return: list of tuples, store number, store name
    """
    pattern = "(?<=inventory = )(.*)"
    store_list = extract_to_json(pattern, html)
    store_list = [(store['storeNumber'], store['storeName']) for store in store_list]
    return store_list


def get_inventories(url: str, stores: list):
    """
    given item url, list of stores, and store_only, return all store inventories
    :param url: str, base product url
    :param stores: list of tuples of store number, store name
    :return: list of tuples, store name, inventory, sorted alphabetically by store
    """
    pattern = '(?s)(?<=inventoryCnt">)(.*?)(?=<)'
    inventories = []
    for store_number, store_name in stores:
        if store_number == '029':
            # skip web store
            continue
        html = get_html(url, store_number)
        data = re.search(pattern, html)
        try:
            inventory = data.group(0).strip()
        except AttributeError as e:
            # No inventoryCnt class found = only avail in store or sold out at location
            mc_logger.error(f'AttributeError: {e}')
        else:
            if inventory != 'Sold Out':
                inventories.append(tuple((store_name, store_number, inventory)))
    inventories.sort(key=lambda store: store[0])
    return inventories


def get_metadata(html: str):
    """
    Given html, return general product data
    :param html: str, raw html
    :return: dict, specified addl_product_attrs
    """
    pattern = "(?s)(?<=dataLayer = \[)(.*?)(?=\];)"
    all_metadata = extract_to_json(pattern, html)
    store_only_flag = 'Available for In-Store Pickup Only.'
    metadata = {
        'price': int(round(float(all_metadata['productPrice']))),
        'store_only': 'Yes' if all_metadata['AvailabilityCode'] == store_only_flag else 'No',
        'mpn': all_metadata['mpn'],
    }
    return metadata


@register('microcenter.com')
def mc_run(submission):
    """
    Given a submission, return a Post object and appropriate markdown
    :param submission: praw.Reddit.submission
    :return: a Post object and appropriate markdown
    """
    url = strip_url(submission.url)

    html = get_html(url)
    metadata = get_metadata(html)

    stores = get_stores(html)
    inventories = get_inventories(url, stores)

    post = Post(submission.fullname,
                metadata.get('mpn'),
                metadata.get('price'),
                datetime.date.today(),
                'microcenter.com',
                )

    markdown = mc_template.build_markdown(inventories, metadata, url)

    return post, markdown


def main():
    pass
    """
    url = 'http://www.microcenter.com/product/501644/HMD_Odyssey_Windows_Mixed_Reality_Headset?storeID=45&gclid=EAIaIQobChMIvrey9tzj2wIVkWV-Ch0eMAjQEAQYASABEgIjL_D_BwE'
    url = strip_url(url)

    html = get_html(url)
    metadata = get_metadata(html)

    stores = get_stores(html)
    inventories = get_inventories(url, stores)

    markdown = mc_template.build_markdown(inventories, metadata, url)

    print(markdown)
    """


if __name__ == '__main__':
    main()


