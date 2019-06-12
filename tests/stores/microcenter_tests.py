import unittest

from src.stores.microcenter import *


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


class MicrocenterSimulation:

    @staticmethod
    def test(url):
        url = strip_url(url)
        page = get_page(url)
        text = page.text

        metadata = get_metadata(text)
        stores = get_stores(text)
        store_data = get_store_data(url, stores)

        markdown = mc_template.build_markdown(store_data, metadata, url)

        print(markdown)

    @staticmethod
    def run_test():
        # Should work
        # url = 'http://www.microcenter.com/product/501644/HMD_Odyssey_Windows_Mixed_Reality_Headset'
        # query_string = '?storeID=45&gclid=EAIaIQobChMIvrey9tzj2wIVkWV-Ch0eMAjQEAQYASABEgIjL_D_BwE'
        # url += query_string
        #
        # Should work
        # url = 'http://www.microcenter.com/product/502941/860_EVO_500GB_MLC_V-NAND_SATA_III_6Gb-s_25_Internal_Solid_State_Driv?storeID=151'
        #
        # Should work
        # url = 'http://www.microcenter.com/single_product_results.aspx?sku=782409&storeID=095'
        #
        # Should work
        # url = 'http://www.microcenter.com/product/477236/BarraCuda_2TB_7200RPM_SATA_III_6Gb-s_35_Internal_Hard_Drive'
        #
        # Should work
        # url = 'https://www.microcenter.com/product/602834/b242-desktop-computer'
        #
        # Should Fail
        # url = 'http://www.microcenter.com/site/brands/brother_storefront.aspx'
        #
        # MicrocenterSimulation.test(url)

        pass


# if __name__ == '__main__':
#     MicrocenterSimulation.run_test()


