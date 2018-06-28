from src.stores.frys import *


class FrysSimulation:

    @staticmethod
    def test(url):
        page = get_page(url)
        content = page.content

        try:
            tree = html.fromstring(content)
        except etree.ParserError as e:
            # Frys mailer/multiproduct links
            frys_logger.error(f'{e.__class__}: {e}')
            return None, None

        price = get_price(tree)
        mpn = get_mpn(tree)

        print(url)
        print(price)
        print(mpn)

    @staticmethod
    def run_test():
        # Should work
        # url = 'https://www.frys.com/product/8760481?site=sr:SEARCH:MAIN_RSLT_PG'
        #
        # Should work
        # url = 'https://www.frys.com/product/9041277?site=sr%3ASEARCH%3AMAIN_RSLT_PG'
        #
        # Should work
        # url = 'https://www.frys.com/product/9331460'
        #
        # Should fail
        # url = 'https://frys.hs.llnwd.net/e1/art/email/112417_fri082tvr_BF1/BF1_web.html#set1'
        #
        # FrysSimulation.test(url)

        pass


if __name__ == '__main__':
    FrysSimulation.run_test()

