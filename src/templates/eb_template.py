from templates import base


def build_markdown(listing_data: dict):
    """

    :param listing_data: dict
    :return: str, markdown formatted
    """

    line_split = '  \n\n'

    lines = [
        get_listing_detail_section(listing_data),
        base.get_footer(listing_data.get('MPN (probably)'))
    ]

    return line_split.join(lines)


def get_listing_detail_section(store_data: dict):
    detail_header = f'Item|Notes\n'
    detail_format = f':-:|:-:\n'

    detail_body = []
    for key, value in store_data.items():
        if value is not None:
            detail_body.append(f'{key}|{value}')

    detail_body = '\n'.join(detail_body)

    return (detail_header
            + detail_format
            + detail_body)


