# -*- coding: utf-8 -*-
# author = Administrator
# date = 2020/6/1 17:37

import os
import unittest
import uiautomator2 as u2
from seldom.logging.log import Log
log = Log()


class U2Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.driver = start_u2_server()

    def setUp(self) -> None:
        if self.driver:
            log.info('u2驱动已加载')
        else:
            self.driver = start_u2_server()


def start_u2_server():
    get_devices_data = get_connected_device()
    device_name = ''.join(get_devices_data[0])
    device_num = get_devices_data[1]

    if device_num == 1:
        log.info('连接设备：' + device_name + ',连接设备数量：' + str(device_num))
        driver = u2.connect(device_name)
        return driver

    elif device_num > 1:
        log.error('连接设备数量>1，请核对需要具体连接的设备后重新执行程序')
        raise Exception('测试设备异常：可用设备大于1')

    else:
        log.error('设备未连接，请连接手机设备后重新执行程序')
        raise Exception('测试设备异常：未连接手机')


def get_connected_device():
    result = os.popen('adb devices')  # 这里通过调用adb devices 命令，获取当前已经连接的设备
    res = result.read()
    i = 0
    j = 0
    device = []
    for line in res.splitlines():
        if 'device' in line:
            i += 1
            if i > 1:
                j += 1
                need_data = line.split('\t')[0]  # 获取当前连接的设备名称，通过split方式截取\t前面的数据
                device.append(need_data)
    return device, j


if __name__ == '__main__':
    d = u2.connect('')
    d.xpath()
    d.click()
    d()
    print(d)