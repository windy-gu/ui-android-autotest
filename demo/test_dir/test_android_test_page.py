import seldom
from android.adb_util import os_popen
from android.u2driver import U2Driver
from android.android_u2_test import U2Test
from pageobject.u2 import Page, PageElement


class MerchantOrderPage(Page):
    """Baidu serach test case"""

    switch_order = {'resourceId': 'com.kh_super.android.supermerchant:id/switch_order'}
    # search_button = PageElement(xpath='//*[@id="su"]')

    switch_order_page = PageElement(describe='自动接单开关', **switch_order)


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
        :return:
        """

        page = MerchantOrderPage(self.driver)
        page.switch_order_page.click()


if __name__ == '__main__':
    seldom.main(debug=True)


