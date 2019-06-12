from src.stores.newegg import *


class NeweggSimulation:

    @staticmethod
    def test(url):
        url = convert_mobile_url(url)
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
        # Should work - mobile
        # url = 'https://m.newegg.com/products/N82E16811352078'
        #
        # Should work - mobile
        # url = 'https://m.newegg.com/products/N82E16814137254?utm_medium=Email&utm_source=IGNEFL062818&cm_mmc=EMC-IGNEFL062818-_-EMC-062818-Index-_-DesktopGraphicsCards-_-14137254-S0A&ignorebbr=1'
        #
        # Should work
        # url = 'https://www.newegg.com/Product/Product.aspx?ignorebbr=1&_ga=2.82317909.2116138168.1529969256-1886606972.1524787829&_gac=1.13765957.1530123833.CjwKCAjw68zZBRAnEiwACw0eYZ1BFZ9T126XdduLyahGFYPMRUljkpIkxPYp7-u3OpkC9cKeqL9rJxoCCcgQAvD_BwE&Item=N82E16824499003'
        #
        # Should work
        # url = 'https://www.newegg.com/p/N82E16813144219?Description=z390&cm_re=z390-_-13-144-219-_-Product'
        #
        # Should fail
        # url = 'https://www.newegg.com/Product/ComboBundleDetails.aspx?ItemList=Combo.3835779'
        #
        # NeweggSimulation.test(url)

        pass


if __name__ == '__main__':
    NeweggSimulation.run_test()

