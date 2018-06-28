from src.stores.newegg import *


class NeweggSimulation:

    @staticmethod
    def test(url):
        page = get_page(url)
        text = page.text

        price = get_price(text)
        mpn = get_mpn(text)

        print(price)
        print(mpn)

    @staticmethod
    def run_test():
        # Should work
        # url = 'https://www.newegg.com/Product/Product.aspx?Item=N82E16813128972&ignorebbr=1'
        #
        # Should work
        # url = 'https://www.newegg.com/Product/Product.aspx?ignorebbr=1&_ga=2.82317909.2116138168.1529969256-1886606972.1524787829&_gac=1.13765957.1530123833.CjwKCAjw68zZBRAnEiwACw0eYZ1BFZ9T126XdduLyahGFYPMRUljkpIkxPYp7-u3OpkC9cKeqL9rJxoCCcgQAvD_BwE&Item=N82E16824499003'
        #
        # Should work
        # url = 'https://www.newegg.com/Product/Product.aspx?Item=N82E16813144154&cm_re=msi_mobo-_-13-144-154-_-Product'
        #
        # Should fail
        # url = 'https://www.newegg.com/Product/ComboBundleDetails.aspx?ItemList=Combo.3835779'
        #
        # NeweggSimulation.test(url)

        pass


if __name__ == '__main__':
    NeweggSimulation.run_test()

