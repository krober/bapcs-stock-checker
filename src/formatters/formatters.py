def build_markdown(inventories: list, metadata: dict):
    """
    given locations(location, inventory) and metadata, return reddit-structured markdown
    :param inventories: list of tuples, (location, inventory)
    :param metadata: dict, should include mpn and price at minimum, optionally store_only
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
        'Newegg': 'https://www.newegg.com/Product/ProductList.aspx?Submit=ENE&DEPA=0&Description='
    }

    meta_section = get_meta_section(metadata)
    inv_section = get_inv_section(inventories) if inventories else 'No inventory found'
    search_links = '|'.join([f'[{site}]({search_sites.get(site)}{metadata.get("mpn")})' for site in search_sites])
    admin = 'Please PM for errors'

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

    return meta_header + meta_format + meta_body


def get_inv_section(inventories: list):
    inv_header = 'Location|Quantity\n'
    inv_format = ':-|-:\n'
    inv_body = '\n'.join([f'{location}|{inventory}' for location, inventory in inventories])

    return inv_header + inv_format + inv_body


if __name__ == '__main__':
    pass

