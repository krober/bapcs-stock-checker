import unittest

from src.stores.microcenter import strip_url


class MicrocenterTests(unittest.TestCase):

    def test_strip_url_storeID_in_middle(self):
        base_url = 'http://www.microcenter.com/product/501644/HMD_Odyssey_Windows_Mixed_Reality_Headset'

        bad_query_string = '?storeID=45&gclid=EAIaIQobChMIvrey9tzj2wIVkWV-Ch0eMAjQEAQYASABEgIjL_D_BwE'
        bad_url = base_url + bad_query_string

        stripped_query_string = '?gclid=EAIaIQobChMIvrey9tzj2wIVkWV-Ch0eMAjQEAQYASABEgIjL_D_BwE'
        stripped_url = base_url + stripped_query_string

        self.assertEqual(stripped_url, strip_url(bad_url))

    def test_strip_url_storeID_at_end(self):
        base_url = 'http://www.microcenter.com/product/501644/HMD_Odyssey_Windows_Mixed_Reality_Headset'

        bad_query_string = '?gclid=EAIaIQobChMIvrey9tzj2wIVkWV-Ch0eMAjQEAQYASABEgIjL_D_BwE&storeID=45'
        bad_url = base_url + bad_query_string

        stripped_query_string = '?gclid=EAIaIQobChMIvrey9tzj2wIVkWV-Ch0eMAjQEAQYASABEgIjL_D_BwE&'
        stripped_url = base_url + stripped_query_string

        self.assertEqual(stripped_url, strip_url(bad_url))

    def test_strip_url_storeID_only(self):
        base_url = 'http://www.microcenter.com/product/501644/HMD_Odyssey_Windows_Mixed_Reality_Headset'

        bad_query_string = '?storeID=45'
        bad_url = base_url + bad_query_string

        stripped_query_string = '?'
        stripped_url = base_url + stripped_query_string

        self.assertEqual(stripped_url, strip_url(bad_url))

    def test_strip_url_storeID_missing_with_query_string(self):
        base_url = 'http://www.microcenter.com/product/501644/HMD_Odyssey_Windows_Mixed_Reality_Headset'

        bad_query_string = '?gclid=EAIaIQobChMIvrey9tzj2wIVkWV-Ch0eMAjQEAQYASABEgIjL_D_BwE'
        bad_url = base_url + bad_query_string

        stripped_query_string = '?gclid=EAIaIQobChMIvrey9tzj2wIVkWV-Ch0eMAjQEAQYASABEgIjL_D_BwE'
        stripped_url = base_url + stripped_query_string

        self.assertEqual(stripped_url, strip_url(bad_url))

    def test_strip_url_storeID_missing_no_query_string(self):
        base_url = 'http://www.microcenter.com/product/501644/HMD_Odyssey_Windows_Mixed_Reality_Headset'

        bad_query_string = ''
        bad_url = base_url + bad_query_string

        stripped_query_string = ''
        stripped_url = base_url + stripped_query_string

        self.assertEqual(stripped_url, strip_url(bad_url))

    def test_strip_url_storeID_with_single_product_results(self):
        base_url = 'http://www.microcenter.com/single_product_results.aspx'

        bad_query_string = '?sku=782409&storeID=095'
        bad_url = base_url + bad_query_string

        stripped_query_string = '?sku=782409&'
        stripped_url = base_url + stripped_query_string

        self.assertEqual(stripped_url, strip_url(bad_url))

    def test_strip_url_storeID_missing_with_single_product_results(self):
        base_url = 'http://www.microcenter.com/single_product_results.aspx'

        bad_query_string = '?sku=782409'
        bad_url = base_url + bad_query_string

        stripped_query_string = '?sku=782409'
        stripped_url = base_url + stripped_query_string

        self.assertEqual(stripped_url, strip_url(bad_url))


