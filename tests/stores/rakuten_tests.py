from src.stores.rakuten import *


class RakutenSimulation:

    @staticmethod
    def test(url):
        page = get_page(url)
        text = page.text
    
        price = get_price(text)
        mpn = get_mpn(text)
    
        print(url)
        print(price)
        print(mpn)

    @staticmethod
    def run_test():
        # Should work
        # url = 'https://www.rakuten.com/shop/beachaudio/product/18851630/'
        #
        # Should work
        # url = 'https://www.rakuten.com/shop/adata/product/AX4U266638G16-DBG/?ranMID=36342&ranEAID=lw9MynSeamY&ranSiteID=lw9MynSeamY-NUY9LaKTHvykGmwGOmTmOQ&scid=af_linkshare&siteID=lw9MynSeamY-NUY9LaKTHvykGmwGOmTmOQ'
        #
        # Should work
        # url = 'https://www.rakuten.com/shop/adata/product/ASU650SS-960GT-C/'
        #
        # Should work
        # url = 'https://www.rakuten.com/shop/platinum-micro/product/CAOPTIXG24C/'
        #
        # Should fail
        # url = 'https://www.rakuten.com/event/10-dollar-off-sitewide/?l-id=promo-10off-headertext'
        #
        # RakutenSimulation.test(url)

        pass


if __name__ == '__main__':
    RakutenSimulation.run_test()

