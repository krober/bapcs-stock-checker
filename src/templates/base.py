def none_to_empty_string(data: str):
    return '' if not data else data


def get_header(metadata: dict):
    mpn = none_to_empty_string(metadata.get('mpn'))
    price = none_to_empty_string(metadata.get('price'))
    store_only = none_to_empty_string(metadata.get('store_only'))

    table_header = 'MPN|Price|Store Only\n'
    table_format = ':-|-:|:-:\n'
    table_body = f'{mpn}|{price}|{store_only}'

    return (table_header
            + table_format
            + table_body)


def get_footer(mpn: str):
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

    search_links = []
    for site, url in search_sites.items():
        search_links.append(f'[{site}]'
                            f'('
                            f'{url}'
                            f'{mpn}'
                            f')')
    search_links = '|'.join(search_links)

    admin = ('Please PM for errors  \n'
             '[See on GitHub](https://github.com/krober/bapcs-stock-checker)')

    return (search_links
            + admin)


