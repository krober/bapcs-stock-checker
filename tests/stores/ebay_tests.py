from src.stores.ebay import *


class EbaySimulation:

    @staticmethod
    def test(url):
        page = get_page(url)
        text = page.text
        content = page.content
        tree = html.fromstring(content)

        listing_data = {
            'Seller': get_seller(tree),
            'Seller Feedback': get_feedback(text),
            'Seller Score': get_score(tree),
            'Ebay Item Number': get_item_number(tree),
            'Free Shipping': 'Yes' if is_free_shipping(tree) else 'No',
            'MPN (probably)': get_mpn(text),
            'Price': get_price(tree),
        }

        product_details = {
            'mpn': listing_data.get('mpn'),
            'price': listing_data.get('price'),
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
        # url = 'https://www.ebay.com/itm/NEW-AMD-RYZEN-7-2700X-8-Core-3-7-GHz-Socket-AM4-105W-YD270XBGAFBOX-Processor/273199602622'
        #
        # Should work
        # url = 'https://www.ebay.com/itm/Best-Buy-Gift-Card-25-50-100-or-150-Fast-Email-delivery/262075905712?var=560853814071&_trkparms=%26rpp_cid%3D5b2894c84de66764007d7240%26rpp_icid%3D56ec4a8ce4b00bcc855a5463'
        #
        # Should work
        # url = 'https://www.ebay.com/itm/Landmann-City-Lights-Memphis-Fire-Pit-Black-/182641297525'
        #
        # Should fail
        # url = 'https://pages.ebay.com/promo/2018/0621/66698.html?_trkparms=%26clkid%3D4767729480946058037'
        #
        # EbaySimulation.test(url)

        pass


if __name__ == '__main__':
    EbaySimulation.run_test()



