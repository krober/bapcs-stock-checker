def build_markdown(locations: list, metadata: dict):
    """
    given locations(location, inventory) and metadata, return reddit-structured markdown
    :param locations: list of tuples, (location, inventory)
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

    mpn = metadata.get('mpn')
    price = metadata.get('price')
    in_store_only = 'Yes' if metadata.get('store_only') else 'No'

    line_split = '  \n\n'

    meta_header = 'MPN|Price|Store Only\n'
    meta_format = ':-|-:|:-:\n'
    meta_body = f'{mpn}|{price}|{in_store_only}'

    inv_header = 'Location|Quantity\n'
    inv_format = ':-|-:\n'
    inv_body = '\n'.join([f'{location}|{inventory}' for location, inventory in locations])

    search_links = 'Find on ' + ' '.join([f'[{site}]({search_sites.get(site)}{mpn})' for site in search_sites])

    admin = 'Please PM for errors'

    lines = [
        meta_header,
        meta_format,
        meta_body,
        line_split,
        inv_header,
        inv_format,
        inv_body,
        line_split,
        search_links,
        line_split,
        admin,
    ]

    return ''.join(lines)


if __name__ == '__main__':
    pass

