from templates import base


def build_markdown(store_data: dict, metadata: dict, url: str):
    """
    given locations(location, inventory) and metadata, return reddit-structured markdown
    :param store_data: dict, enabled columns + (location, inventory, open_box)
    :param metadata: dict, should include mpn and price at minimum, optionally store_only
    :param url: str, base url to mc product
    :return: str, markdown formatted
    """
    inv_section = get_inv_section(store_data, url)

    line_split = '  \n\n'

    lines = [
        base.get_header(metadata),
        inv_section,
        base.get_footer(metadata.get('mpn'))
    ]

    return line_split.join(lines)


def get_inv_section(store_data: dict, url: str):
    show_open_box = store_data.get('Open Box', False)

    open_box_header = '|Open Box' if show_open_box else ''
    open_box_format = '|-:' if show_open_box else ''

    inv_header = f'Location|Quantity{open_box_header}\n'
    inv_format = f':-|-:{open_box_format}\n'

    query_string = '&storeID=' if '?' in url else '?storeID='

    inv_body = []
    for store_name, store_number, inventory, open_box in store_data.get('inventories'):
        inventory = base.none_to_empty_string(inventory)
        open_box = base.none_to_empty_string(open_box)

        line = (f'[{store_name}]({url}{query_string}{store_number})'
                f'|{inventory}')

        if show_open_box:
            line += '|'

        if open_box != '':
            line += f'from {open_box}'

        inv_body.append(line)
    inv_body = '\n'.join(inv_body)

    return (inv_header
            + inv_format
            + inv_body)


