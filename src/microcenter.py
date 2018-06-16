import json
import re
import requests
import time


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


def extract_from_html(pattern: str, html: str):
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
    store_list = extract_from_html(pattern, html)
    store_list = [(store['storeNumber'], store['storeName']) for store in store_list]
    return store_list


def get_inventories(url: str, stores: list, in_store_only: bool):
    """
    given item url, list of stores, and store_only, return all store inventories
    :param url: str, base product url
    :param stores: list of tuples of store number, store name
    :param in_store_only: bool, is product in store only?
    :return: list of tuples, store name, inventory, sorted alphabetically by store
    """
    iter_for_test = 0
    pattern = '(?s)(?<=inventoryCnt">)(.*?)(?=<)'
    inventories = []
    for store_number, store_name in stores:
        if iter_for_test == 4:
            break
        if store_number == '029' and in_store_only:  # skip web store, <span> doesn't exist and will error
            inventories.append(tuple((store_name, 'In Store Only')))
        else:
            html = get_html(url, store_number)
            inventory = re.search(pattern, html).group(0).strip()
            inventories.append(tuple((store_name, inventory)))
        time.sleep(2)  # don't spam MC server?
        iter_for_test += 1
    inventories.sort(key=lambda store: store[0])
    return inventories


def get_metadata(html: str):
    """
    Given product data, return specific product attrs
    :param html: str, raw html
    :return: dict, specified addl_product_attrs
    """
    pattern = "(?s)(?<=dataLayer = \[)(.*?)(?=\];)"
    all_metadata = extract_from_html(pattern, html)
    metadata = {
        'price': all_metadata['productPrice'],
        'store_only': True if all_metadata['AvailabilityCode'] == 'Available for In-Store Pickup Only.' else False,
        'mpn': all_metadata['mpn'],
    }
    return metadata


def mc_run(url: str):
    """
    Given a url, parse and return inventories by location and product metadata
    :param url: str, url to MC product
    :return: tuple, list of tuples of inventories by location; metadata dict
    """
    html = get_html(url)
    metadata = get_metadata(html)

    stores = get_stores(html)
    inventories = get_inventories(url, stores, metadata['store_only'])

    return inventories, metadata


if __name__ == '__main__':
    pass


