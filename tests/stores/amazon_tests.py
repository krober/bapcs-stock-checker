from src.stores.amazon import *


class AmazonSimulation:

    @staticmethod
    def test(url):
        page = get_page(url)
        text = page.text
        content = page.content
        tree = html.fromstring(content)

        price = get_price(tree)
        mpn = get_mpn(text)

        print(price)
        print(mpn)

    @staticmethod
    def run_test():
        # Should work
        # url = 'https://www.amazon.com/Crucial-MX500-NAND-SATA-Internal/dp/B077SF8KMG'
        #
        # Should work
        # url = 'https://www.amazon.com/gp/product/B073TQKNF2/'
        #
        # Should work
        # url = 'https://www.amazon.com/RIPJAWS-KM570-Cherry-Speed-Silver/dp/B01LZEVDKI/'
        #
        # Should work
        # url = 'https://www.amazon.com/Kingston-120GB-Solid-SA400S37-120G/dp/B01N6JQS8C/ref=mp_s_a_1_6?ie=UTF8&qid=1528906162&sr=8-6&pi=AC_SX236_SY340_QL65&keywords=ssd&dpPl=1&dpID=41EjY-AhQUL&ref=plSrch'
        #
        # Should work
        # url = 'https://www.amazon.com/TP-Link-RangeBoost-Technology-Archer-A2300/dp/B0751RK6XZ/ref=sr_1_1?m=A3C0IBSA2XBL9N&s=merchant-items&ie=UTF8&qid=1528439208&sr=1-1&refinements=p_4%3ATP-Link&dpID=51LmWDKvBnL&preST=_SX300_QL70_&dpSrc=srch'
        #
        # Should fail
        # url = 'https://www.amazon.com/Home-Audio-Electronics/b/ref=nav_shopall_hat?ie=UTF8&node=667846011'
        #
        AmazonSimulation.test(url)

        pass


if __name__ == '__main__':
    AmazonSimulation.run_test()



