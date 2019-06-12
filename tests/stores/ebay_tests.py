from src.stores.ebay import *


class EbaySimulation:

    @staticmethod
    def test(url):
        url = convert_pages_url(url)
        page = get_page(url)
        text = page.text
        content = page.content
        tree = html.fromstring(content)

        listing_data = {
            'Seller': get_seller(tree),
            'Seller Feedback': get_feedback(text),
            'Seller Score': get_score(tree),
            'Ebay Item Number': get_item_number(tree),
            'MPN (probably)': get_mpn(text),
            'Price': get_price(tree),
        }

        product_details = {
            'mpn': listing_data.get('MPN (probably)'),
            'price': listing_data.get('Price'),
        }

        print(listing_data)
        print(product_details)

        if (listing_data.get('Seller') is None or
                listing_data.get('Seller Feedback') is None or
                listing_data.get('Seller Score') is None):
            markdown = None
        else:
            markdown = eb_template.build_markdown(listing_data)

        print(markdown)

    @staticmethod
    def run_test():
        # Should work
        # url = 'https://www.ebay.com/itm/263771931884?ViewItem=&item=263771931884'
        #
        # Should work
        # url = 'https://www.ebay.com/itm/Best-Buy-Gift-Card-25-50-100-or-150-Fast-Email-delivery/262075905712?var=560853814071&_trkparms=%26rpp_cid%3D5b2894c84de66764007d7240%26rpp_icid%3D56ec4a8ce4b00bcc855a5463'
        #
        # Should work
        # url = 'https://www.ebay.com/itm/Dell-Latitude-5590-i7-8650U-32GB-Ram-512GB-SSD-IPS-1080p/273880535372?hash=item3fc48d514c:g:HycAAOSwMMJc8JJJ'
        #
        # Should work - /p/ link
        # url = 'https://www.ebay.com/p/GIGABYTE-AORUS-GeForce-GTX-1080-Ti-11GB-Video-Card-GV-N108TAORUS-11GD/20019368148?iid=382497154524&_trkparms=5373%3A0%7C5374%3AFeatured'
        #
        # Should fail
        # url = 'https://pages.ebay.com/promo/2018/0621/66698.html?_trkparms=%26clkid%3D4767729480946058037'
        #
        # EbaySimulation.test(url)

        pass


if __name__ == '__main__':
    EbaySimulation.run_test()



