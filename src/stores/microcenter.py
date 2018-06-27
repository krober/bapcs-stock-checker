import json
import re
import requests

from lxml import html

from stores.registration import register
from templates import mc_template
from logger import logger


mc_logger = logger.get_logger('Microcenter', './logfile.log')


def strip_url(url: str):
    """
    Given a Microcenter URL, if query string is present, strip it and return
    stripped string.  Titles of products should not contain '?'
    :param url: str, microcenter url
    :return: str, stripped of query string as necessary
    """
    if 'storeID=' in url:
        begin_id = url.find('storeID=')
        end_id = begin_id + 11  # len('storeID=095')
        url = url[:begin_id] + url[end_id:]
    mc_logger.info(f'url: {url}')
    return url


def get_page(url: str, store_num: str= '095'):
    """
    Given a Microcenter URL, return request object
    :param url: str, microcenter url
    :param store_num: str, store number as string, defaults to MO - Brentwood
    :return: requests.model.Response, html from url
    """
    headers = {
        'Cookie': 'storeSelected=' + store_num,
        'DNT': '1',
        'Host': 'www.microcenter.com',
    }
    return requests.get(url, headers=headers)


def extract_from_json(pattern: str, text: str):
    """
    Given raw Microcenter HTML and search pattern, find, format,
    and return matching python dictionary
    :param pattern: str, regex to search for in html
    :param text: str, raw html
    :return: dict, from html based on pattern
    """
    data = re.search(pattern, text)
    data_json = data.group(0)\
                    .strip()\
                    .replace("'", "\"")
    return json.loads(data_json)


def get_stores(text: str):
    """
    Given mc html, return list stores
    :param text: str, raw html
    :return: list of tuples, store name, store number
    """
    pattern = "(?<=inventory = )(.*)"
    stores = extract_from_json(pattern, text)
    stores_admin = []
    for store in stores:
        name = store.get('storeName')
        number = store.get('storeNumber')
        if number == '029':
            # skip web store
            continue
        store_admin = (name, number)
        if None not in store_admin:
            stores_admin.append(store_admin)
    return stores_admin


def get_inventory(tree: html.HtmlElement):
    """
    Given html.HtmlElement for single MC store, parse
    and return inventory count
    :param tree: html.HtmlElement
    :return: str, inventory, ex '9 in stock'; None if parse error
    """
    path = '//span[@class="inventoryCnt"]'
    try:
        inventory = tree.xpath(path)[0].text
    except IndexError as e:
        # No inventoryCnt class found = sold out at location
        mc_logger.error(f'{e.__class__}: {e}')
    else:
        if inventory != 'Sold Out':
            return inventory
    return None


def get_open_box(tree: html.HtmlElement):
    """
    Give html.HtmlElement for single MC store, parse
    and return open box price
    :param tree: html.HtmlElement
    :return: str, open box price, ex '$249.99'; None if doesn't exist
    """
    path = '//span[@id="opCostNew"]'
    try:
        open_box = tree.xpath(path)[0].text
    except IndexError as e:
        # No opCostNew id found = no open box available at location
        mc_logger.info(f'{e.__class__}: {e}')
    else:
        return open_box
    return None


def get_store_data(url: str, stores: list):
    """
    Given item url and list of stores, return all store inventories
    :param url: str, base product url
    :param stores: list of tuples of store name, store number
    :return: dict, enabled columns & inventories as list of tuples
    """
    store_data = {
        'Location': True,
        'Quantity': True,
        'Open Box': False,
        'inventories': [],
    }
    for store_name, store_number in stores:
        page = get_page(url, store_number)
        tree = html.fromstring(page.content)
        inventory = get_inventory(tree)
        open_box = get_open_box(tree)
        if open_box is not None:
            store_data['Open Box'] = True
        if inventory is not None or open_box is not None:
            line = (store_name, store_number, inventory, open_box)
            store_data['inventories'].append(line)
    store_data['inventories'].sort(key=lambda store: store[0])
    return store_data


def get_metadata(text: str):
    """
    Given html, return general product data
    :param text: str, raw html
    :return: dict, specified metadata
    """
    pattern = "(?s)(?<=dataLayer = \[)(.*?)(?=\];)"
    all_metadata = extract_from_json(pattern, text)
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
    Given a submission, return product details and appropriate markdown
    :param submission: praw.Reddit.submission
    :return: dict, product_details and str, appropriate markdown
    """
    url = strip_url(submission.url)
    page = get_page(url)
    text = page.text

    metadata = get_metadata(text)
    stores = get_stores(text)
    store_data = get_store_data(url, stores)

    markdown = mc_template.build_markdown(store_data, metadata, url)

    product_details = {
        'mpn': metadata.get('mpn'),
        'price': metadata.get('price'),
    }

    return product_details, markdown


def main():

    # url = 'http://www.microcenter.com/product/501644/HMD_Odyssey_Windows_Mixed_Reality_Headset'
    # query_string = '?storeID=45&gclid=EAIaIQobChMIvrey9tzj2wIVkWV-Ch0eMAjQEAQYASABEgIjL_D_BwE'
    # url += query_string
    # url = strip_url(url)
    #
    # url = 'http://www.microcenter.com/product/502941/860_EVO_500GB_MLC_V-NAND_SATA_III_6Gb-s_25_Internal_Solid_State_Driv?storeID=151'
    # url = strip_url(url)
    #
    # url = 'http://www.microcenter.com/single_product_results.aspx?sku=782409&storeID=095'
    # url = strip_url(url)
    #
    # url = 'http://www.microcenter.com/single_product_results.aspx?sku=782409&storeID=095&some=otherStuff'
    # url = strip_url(url)
    #
    # url = 'http://www.microcenter.com/single_product_results.aspx?sku=782409'
    # url = strip_url(url)
    #
    # url = 'http://www.microcenter.com/product/477236/BarraCuda_2TB_7200RPM_SATA_III_6Gb-s_35_Internal_Hard_Drive'
    # url = strip_url(url)
    #
    # url = 'http://www.microcenter.com/product/503281/Inspiron_15_3567_156_Laptop_Computer_-_Black'
    # url = strip_url(url)
    #
    # page = get_page(url)
    # text = page.text
    #
    # metadata = get_metadata(text)
    # stores = get_stores(text)
    # store_data = get_store_data(url, stores)
    #
    # markdown = mc_template.build_markdown(store_data, metadata, url)
    #
    # print(markdown)

    pass


if __name__ == '__main__':
    main()


