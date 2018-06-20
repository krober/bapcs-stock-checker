import datetime
import re
import requests

from models.post import Post


def get_html(url: str):
    """
    Given a newegg URL, return raw HTML
    :param url: str, newegg url
    :return: str, html from url
    """
    headers = {
        'DNT': '1',
        'Host': 'www.newegg.com',
    }
    return requests.get(url, headers=headers).text


def get_mpn(html: str):
    """
    Given newegg html, return mpn
    :param html: str, raw html
    :return: str, mpn
    """
    pattern = "(?<=product_model:\[\\')(.*)(?=\\'\])"
    mpn = re.search(pattern, html).group(0)
    return mpn


def get_price(html: str):
    """
    Given newegg html, return int price
    :param html: str, raw html
    :return: int, price, rounded
    """
    pattern = "(?<=product_sale_price:\[\\')(.*)(?=\\'\])"
    price = re.search(pattern, html).group(0)
    return int(round(float(price)))


def ne_run(submission):
    """
    Given a submission, return a Post object
    :param submission: praw.Reddit.submission
    :return: Post
    """
    # TODO: add markdown
    url = submission.url

    html = get_html(url)

    mpn = get_mpn(html)
    price = get_price(html)

    post = Post(submission.fullname,
                mpn,
                price,
                datetime.date.today(),
                'newegg.com',
                )

    return post, None


def main():
    """
    url = 'https://www.newegg.com/Product/Product.aspx?Item=N82E16813128972&ignorebbr=1'
    post, markdown = ne_run(url)

    print(post)

    if markdown is None:
        print('md is none')
    else:
        print('md aint none')
    """
    pass


if __name__ == '__main__':
    main()


