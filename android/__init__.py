# -*- coding: utf-8 -*-
# author = Administrator
# date = 2020/5/30 16:16

import os
import uiautomator2 as u2
from seldom.logging.log import Log


class Android():
    def __init__(self):
        self.serial_number = os.popen('adb devices').read().split('\n')[1].split('\t')[0]


class GetPhoneInfo(Android):
    """
    获取android手机相关参数
    """
    def screen_state(self):
        """
        通过adb命令获取手机屏幕的状态信息
        :return:
        """
        data = os.popen('adb -s ' + self.serial_number +
                        ' shell dumpsys window policy|find "screenState"').read().strip()
        return data

    def phone_brand(self):
        """
        通过adb命令获取手机品牌信息
        :return:
        """
        brand = os.popen('adb -s ' + self.serial_number +
                         ' shell getprop ro.product.brand').read().strip()
        return brand

    def phone_model(self):
        """
        通过adb命令获取手机型号信息
        :return:
        """
        model = os.popen('adb -s ' + self.serial_number +
                         ' shell getprop ro.product.model').read().strip()
        return model

    def phone_android_version(self):
        """
        通过adb命令获取手机-android 系统版本
        :return:
        """
        version = os.popen('adb -s ' + self.serial_number +
                           ' shell getprop ro.build.version.release').read().strip()
        return version

    def phone_resolution(self):
        """
        通过adb命令获取手机分辨率
        :return:
        """
        resolution = ''
        data = os.popen('adb -s ' + self.serial_number + ' shell wm size').readlines()
        for n in data:
            if 'Physical' in n:
                resolution = n.split(':')[1].strip()
                break
        return resolution

    def phone_info(self):
        """
        通过adb命令获取手机相关信息
        :return:
        """
        info = os.popen('adb -s ' + self.serial_number +
                        ' shell "getprop | grep product"').read().strip().replace('[', '').replace(']', '')
        return info

    def phone_imei(self):
        """
        通过adb命令获取手机imei信息
        :return:
        """
        imei = ''
        data = os.popen('adb -s ' + self.serial_number + ' shell service call iphonesubinfo 1').readlines()
        for n in data:
            if 'Result' in n:
                continue
            else:
                imei = imei + n.strip().split("'")[1]
        imei = imei.replace('.', '').strip()
        return imei

    def phone_serial_number(self):
        """
        通过adb命令获取手机 serial_number信息，即：devices Id
        :return:
        """
        return self.serial_number


class Page(object):

    def __init__(self, driver):
        self.driver = driver
        self.log = Log()

    def click_element(self, **kwargs):
        self.find_element(**kwargs)
        by, value = next(iter(kwargs.items()))
        if self.driver(**kwargs).exists:
            self.driver(**kwargs).click()
            self.log.info('点击元素,method:{}; value:{}'.format(by, value))
        else:
            self.log.error('Something error')
            pass
        # pass

    def find_element(self, index=0, **kwargs):
        if not kwargs:
            raise ValueError("Please specify a locator")
        if len(kwargs) > 1:
            raise ValueError("Please specify only one locator")
        by, value = next(iter(kwargs.items()))




if __name__ == '__main__':
    # test_dict = {'text': '123'}
    # test = GetPhoneInfo()
    # test.click_element(**test_dict)
    u = u2.connect('WSZPZDSCZTIVJ7E6')
    u.app_start('com.kh_super.android.supermerchant')
    a = GetPhoneInfo()
    print(a.phone_brand())
    print(a.phone_model())
    print(a.phone_imei())
    print(a.phone_serial_number())
    print(a.phone_android_version())
    print(a.phone_resolution())
