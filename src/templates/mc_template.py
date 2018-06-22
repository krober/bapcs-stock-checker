from templates import base


def build_markdown(inventories: list, metadata: dict, url: str):
    """
    given locations(location, inventory) and metadata, return reddit-structured markdown
    :param inventories: list of tuples, (location, inventory)
    :param metadata: dict, should include mpn and price at minimum, optionally store_only
    :param url: str, base url to mc product
    :return: str, markdown formatted
    """
    inv_section = get_inv_section(inventories, url)

    line_split = '  \n\n'

    lines = [
        base.get_header(metadata),
        inv_section,
        base.get_footer(metadata.get('mpn'))
    ]

    return line_split.join(lines)


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


