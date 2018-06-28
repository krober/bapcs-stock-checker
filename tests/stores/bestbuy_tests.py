from src.stores.bestbuy import *


class BestBuySimulation:

    @staticmethod
    def test(url):
        page = get_page(url)
        text = page.text
        content = page.content
        tree = html.fromstring(content)

        price = get_price(text)
        mpn = get_mpn(tree)

        print(url)
        print(price)
        print(mpn)

    @staticmethod
    def run_test():
        # Should work
        # url = 'https://www.bestbuy.com/site/searchpage.jsp?id=pcat17071&st=logitech+g'
        #
        # Should work
        # url = 'https://www.bestbuy.com/site/dell-27-led-qhd-gsync-monitor-black/5293502.p?skuId=5293502'
        #
        # Should work
        # url = 'https://www.bestbuy.com/site/hp-omen-by-hp-desktop-intel-core-i5-8gb-memory-nvidia-geforce-gtx-1060-1tb-hard-drive-brushed-aluminum/5759916.p?skuId=5759916'
        #
        # Should work
        # url = 'https://www.bestbuy.com/site/cyberpowerpc-gamer-ultra-vr-desktop-amd-ryzen-7-series-16gb-memory-nvidia-geforce-gtx-1070-120gb-solid-state-drive-1tb-hdd-black/6092500.p'
        #
        # Should fail
        # url = 'https://www.bestbuy.com/site/home-appliances/refrigerators/abcat0901000.c?id=abcat0901000'
        #
        # BestBuySimulation.test(url)

        pass


if __name__ == '__main__':
    BestBuySimulation.run_test()


