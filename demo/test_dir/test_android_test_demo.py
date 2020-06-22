import seldom
from android.adb_util import os_popen
from android.android_u2_test import U2Test
from android.u2driver import U2Driver


class MerchantOrderPage(U2Driver):
    """Baidu serach test case"""

    switch_order = {'resourceId': 'com.kh_super.android.supermerchant:id/switch_order'}
    # search_button = PageElement(xpath='//*[@id="su"]')

    def click_button(self):
        self.click_element(**self.switch_order)


class MerchantTest(U2Test):
    """

    """

    # @data([
    #     (1, 'seldom'),
    #     (2, 'selenium'),
    #     (3, 'unittest'),
    # ])
    def test_click_switch(self):
        """
         used parameterized test
        :param name: case name
        :param search_key: search keyword
        :return:
        """

        page = MerchantOrderPage(self.driver)
        page.click_button()


if __name__ == '__main__':
    seldom.main(debug=True)


