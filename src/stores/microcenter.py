import json
import re
import requests

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


def get_inventory(html: str):
    pattern = '(?s)(?<=inventoryCnt">)(.*?)(?=<)'
    data = re.search(pattern, html)
    try:
        inventory = data.group(0).strip()
    except AttributeError as e:
        # No inventoryCnt class found = only avail in store or sold out at location
        mc_logger.error(f'{e.__class__}: {e}')
    else:
        if inventory != 'Sold Out':
            return inventory
    return None


def get_open_box(html: str):
    pattern = '(?s)(?<=opCostNew">)(.*?)(?=<)'
    data = re.search(pattern, html)
    try:
        open_box = data.group(0).strip()
    except AttributeError as e:
        # No opCostNew id found = no open box available at location
        mc_logger.error(f'{e.__class__}: {e}')
    else:
        return open_box
    return None


def get_store_data(url: str, stores: list):
    """
    given item url, list of stores, return all store inventories
    :param url: str, base product url
    :param stores: list of tuples of store number, store name
    :return: dict, enabled columns & inventories as tuple
    """
    store_data = {
        'Location': True,
        'Quantity': True,
        'Open Box': False,
    }
    inventories = []
    for store_number, store_name in stores:
        if store_number == '029':
            # skip web store
            continue
        html = get_html(url, store_number)
        inventory = get_inventory(html)
        open_box = get_open_box(html)
        if open_box is not None:
            store_data['Open Box'] = True
        if inventory is not None or open_box is not None:
            line = (store_name, store_number, inventory, open_box)
            inventories.append(line)
    inventories.sort(key=lambda store: store[0])
    store_data['inventories'] = inventories
    return store_data


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
    Given a submission, return product details and appropriate markdown
    :param submission: praw.Reddit.submission
    :return: dict, product_details and str, appropriate markdown
    """
    url = strip_url(submission.url)
    html = get_html(url)

    metadata = get_metadata(html)
    stores = get_stores(html)
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
    # html = get_html(url)
    # metadata = get_metadata(html)
    #
    # stores = get_stores(html)
    # store_data = get_store_data(url, stores)
    #
    # markdown = mc_template.build_markdown(store_data, metadata, url)
    #
    # print(markdown)

    pass


if __name__ == '__main__':
    main()


