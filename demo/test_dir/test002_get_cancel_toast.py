import seldom
from android.adb_util import os_popen
from android.u2driver import U2Driver
from android.android_u2_test import U2BaseCase


class ProcessingPage(U2Driver):
    """Baidu serach test case"""

    processing_btn = {'text': 'Processing'}
    set_prepared = {'resourceId': 'com.kh_super.android.supermerchant:id/btn_process_status'}
    # switch_order = {'resourceId': 'com.kh_super.android.supermerchant:id/switch_order'}

    def click_button(self):
        self.click_element(**self.processing_btn)
        self.click_element(**self.set_prepared)


class ProcessingTest(U2BaseCase):
    """
    测试案例
    """

    # @data([
    #     (1, 'seldom'),
    #     (2, 'selenium'),
    #     (3, 'unittest'),
    # ])
    def test_get_cancel_toast(self):
        """
         used parameterized test
        :return:
        """

        page = ProcessingPage(self.driver)
        # page.click_element(**page.switch_order)
        page.click_button()


if __name__ == '__main__':
    seldom.main(debug=True)


