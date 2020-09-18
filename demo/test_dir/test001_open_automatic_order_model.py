import seldom
from android.adb_util import os_popen
from android.android_u2_test import U2BaseCase
from android.u2driver import U2Driver
from pageobject.u2 import Page, PageElement


class NewOrderPage(Page):
    """Baidu serach test case"""

    # processing_btn = {'text': 'processing'}
    # set_prepared = {'resourceId': 'com.kh_super.android.supermerchant:id/switch_order'}
    switch_order = {'resourceId': 'com.kh_super.android.supermerchant:id/switch_order'}
    # search_button = PageElement(xpath='//*[@id="su"]')

    automatic_order_switch = PageElement(**switch_order)


class NewOrderTest(U2BaseCase):
    """
    打开/关闭自动接单功能
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

        page = NewOrderPage(self.driver)
        page.automatic_order_switch.click(text='自动接单开关')


if __name__ == '__main__':
    seldom.main(debug=True)


