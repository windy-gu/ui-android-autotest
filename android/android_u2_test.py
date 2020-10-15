# -*- coding: utf-8 -*-
# author = Administrator
# date = 2020/6/1 17:37

import time
import unittest
import uiautomator2 as u2
from seldom.logging.log import Log
from android.u2driver import U2Driver
from android.public_util import Config
from android.adb_util import check_package_install_state, check_package_process_state, os_popen
log = Log()


class U2BaseCase(unittest.TestCase, U2Driver):
    conf = Config()
    test_package = conf.get_config_info(section='android_test', option='auto_test_package')
    log = Log()

    @classmethod
    def setUpClass(cls) -> None:
        cls.driver = start_u2_server()

        if not check_package_install_state(cls.test_package):
            # cls.install_app_url() 待补充
            pass

    def setUp(self) -> None:
        if self.driver:
            self.log.info('校验当前连接设备是否具备执行自动化测试条件')
        else:
            self.driver = start_u2_server()

        if not check_screen_state():
            # 判断当前手机屏幕是否处于关闭状态，若关闭则执行上滑解锁的操作
            dr = U2Driver(self.driver)
            dr.swipe_up()

        if not check_package_process_state(self.test_package):
            self.start_app(self.test_package)


def start_u2_server():
    get_devices_data = get_connected_device()
    device_name = ''.join(get_devices_data[0])
    device_num = get_devices_data[1]

    if device_num == 1:
        print('连接设备：' + device_name + ',连接设备数量：' + str(device_num))
        driver = u2.connect(device_name)
        return driver

    elif device_num > 1:
        print('连接设备数量>1，请核对需要具体连接的设备后重新执行程序')
        raise Exception('测试设备异常：可用设备大于1')

    else:
        print('设备未连接，请连接手机设备后重新执行程序')
        raise Exception('测试设备异常：未连接手机')


def get_connected_device():
    res = os_popen(data='adb devices')  # 这里通过调用adb devices 命令，获取当前已经连接的设备
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


def check_screen_state():
    screen_state = False
    screen_state_data = os_popen(data='adb shell "dumpsys window policy|grep screenState"')

    if 'screenState=SCREEN_STATE_ON' in screen_state_data or 'screenState=2' in screen_state_data:
        log.info('当前手机屏幕状态：Screen On')
        screen_state = True
        return screen_state

    elif 'screenState=SCREEN_STATE_OFF' in screen_state_data or 'screenState=0' in screen_state_data:
        log.info('当前手机屏幕状态：Screen Off')
        os_popen(data='adb shell input keyevent 26')
        log.info('adb 命令唤醒屏幕')
        time.sleep(1)
        return screen_state

    else:
        log.error('Something error')
        raise Exception('Something error')

