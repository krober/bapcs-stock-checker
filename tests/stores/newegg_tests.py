import requests
import unittest

from src.stores.newegg import get_mpn


TEST_DB = 'test.db'


class TestNeweggFunctions(unittest.TestCase):

    def test_get_mpn_static_html(self):
        # Perform on text file in same dir to use static data
        """
        with open('newegg_test_html.txt', 'r') as f:
            html = f.read()
        mpn = get_mpn(html)
        self.assertEqual(mpn, 'GA-Z270XP-SLI')
        """

    def test_get_mpn_web_html(self):
        """
        Perform test on url, data may be dynamic and need to be checked
        Must momentarily reconfigure newegg.py to not use Post model due to db usage
        """
        html = requests.get('https://www.newegg.com/Product/Product.aspx?Item=N82E16813128972&ignorebbr=1').text
        mpn = get_mpn(html)
        self.assertEqual(mpn, 'GA-Z270XP-SLI')


if __name__ == '__main__':
    unittest.main()


