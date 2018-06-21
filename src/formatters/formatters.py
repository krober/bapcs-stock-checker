def build_markdown(inventories: list, metadata: dict, url: str):
    """
    given locations(location, inventory) and metadata, return reddit-structured markdown
    :param inventories: list of tuples, (location, inventory)
    :param metadata: dict, should include mpn and price at minimum, optionally store_only
    :param url: str, base url to mc product
    :return: str, markdown formatted
    """
    search_sites = {
        'Google': 'https://www.google.com/search?q=',
        'PCPP': 'https://pcpartpicker.com/search/?q=',
        'UserBench': 'http://userbenchmark.com/Search?searchTerm=',
        'Ebay': 'https://www.ebay.com/sch/i.html?_nkw=',
        'Amazon': 'https://www.amazon.com/s/keywords=',
        'Frys': 'https://www.frys.com/search?query_string=',
        'BestBuy': 'https://www.bestbuy.com/site/searchpage.jsp?st=',
        'Newegg': 'https://www.newegg.com/Product/ProductList.aspx?Submit=ENE&DEPA=0&Description=',
    }

    meta_section = get_meta_section(metadata)
    inv_section = get_inv_section(inventories, url) if inventories else 'No inventory found'

    search_links = []
    for site in search_sites:
        search_links.append(f'[{site}]({search_sites.get(site)}{metadata.get("mpn")})')
    search_links = '|'.join(search_links)

    admin = ('Please PM for errors  \n'
             '[See on GitHub](https://github.com/krober/bapcs-stock-checker)')

    line_split = '  \n\n'

    lines = [
        meta_section,
        inv_section,
        search_links,
        admin,
    ]

    return line_split.join(lines)


def get_meta_section(metadata: dict):
    mpn = metadata.get('mpn')
    price = metadata.get('price')
    store_only = metadata.get('store_only')

    meta_header = 'MPN|Price|Store Only\n'
    meta_format = ':-|-:|:-:\n'
    meta_body = f'{mpn}|{price}|{store_only}'

    return (meta_header
            + meta_format
            + meta_body)


def get_inv_section(inventories: list, url: str):
    inv_header = 'Location|Quantity\n'
    inv_format = ':-|-:\n'

    inv_body = []
    for name, number, inventory in inventories:
        inv_body.append(f'[{name}]({url}?storeID={number})|{inventory}')
    inv_body = '\n'.join(inv_body)

    return (inv_header
            + inv_format
            + inv_body)


if __name__ == '__main__':
    pass

