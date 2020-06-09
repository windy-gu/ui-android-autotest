# -*- coding: utf-8 -*-
# author = Administrator
# date = 2020/6/2 10:46
import time
from seldom.logging.log import Log

LOCATOR_LIST = [
    "text",
    "textContains",
    "textMatches",
    "textStartsWith",
    "className",
    "classNameMatches",
    "description",
    "descriptionContains",
    "descriptionMatches",
    "descriptionStartsWith",
    "checkable",
    "checked",
    "clickable",
    "longClickable",
    "scrollable",
    "enabled",
    "focusable",
    "focused",
    "selected",
    "packageName",
    "packageNameMatches",
    "resourceId",
    "resourceIdMatches",
    "index",
    "instance",
]


class U2Driver(object):
    def __init__(self, driver):
        self.driver = driver
        self.log = Log()
        self.size = self.driver.window_size()
        self.width = self.size[0]
        self.height = self.size[1]

    def install_app_url(self, url: str):
        """
        通过url地址安装app
        :param url:
        :return:
        """
        self.driver.app_install(url)
        self.log.info('通过url链接安装app，链接地址：%s' % url)

    def start_app(self, package: str):
        """
        通过package，启动app进程
        :param package:
        :return:
        """
        self.driver.app_start(package)
        self.log.info('通过package名称，启动app进程，package：%s' % package)

    def stop_app(self, package: str):
        """
        通过package，关闭app进程
        :param package:
        :return:
        """
        self.driver.app_stop(package)
        self.log.info('通过package名称，关闭app进程，package：%s' % package)

    def clear_app(self, package: str):
        """
        通过package，清除app数据
        :param package:
        :return:
        """
        self.driver.app_clear(package)
        self.log.info('通过package名称，清除app数据，package：%s' % package)

    def stop_all(self, excludes: list = None):
        """
        关闭所有后台进行，除了excludes（包名）
        :param excludes:
        :return:
        """
        if excludes:
            self.driver.app_stop_all(excludes=excludes)
        else:
            self.driver.app_stop_all()

    def get_app_info(self, package: str):
        """

        :param package:
        :return:
        """
        info = self.driver.app_info(package)
        return info

    def pull(self, file: str, local: str):
        self.driver.pull(file, local)

    def push(self, file: str, local: str):
        self.driver.push(file, local, mode=0o755)

    def screen_on(self):
        self.driver.screen_on()

    def screen_off(self):
        self.driver.screen_off()
        
    def swipe_up(self, wait_time=0.1, times=1):
        """向上滑动屏幕"""
        x1 = self.width * 0.5
        y1 = self.height * 0.75
        y2 = self.height * 0.25
        self.log.info('向上滑动屏幕:%s次' % times)
        for i in range(times):
            self.driver.drag(x1, y1, x1, y2, wait_time)
            time.sleep(1)

    def swipe_down(self, wait_time=0.1, times=1):
        """向下滑动屏幕"""
        x1 = self.width * 0.5
        y1 = self.height * 0.25
        y2 = self.height * 0.75
        self.log.info('向下滑动屏幕:%s次' % times)
        for i in range(times):
            self.driver.drag(x1, y1, x1, y2, wait_time)
            time.sleep(1)

    def swipe_left(self, wait_time=0.1, times=1):
        """向左滑动屏幕"""
        x1 = self.width * 0.85
        y1 = self.height * 0.5
        x2 = self.width * 0.15
        self.log.info('向左滑动屏幕:%s次' % times)
        for i in range(times):
            self.driver.drag(x1, y1, x2, y1, wait_time)
            time.sleep(1)

    def swipe_right(self, wait_time=0.1, times=1):
        """向右滑动屏幕"""
        x1 = self.width * 0.25
        y1 = self.height * 0.5
        x2 = self.height * 0.75
        self.log.info('向右滑动屏幕:%s次' % times)
        for i in range(times):
            self.driver.drag(x1, y1, x2, y1, wait_time)
            time.sleep(1)

    def click_element(self, **kwargs):
        self.find_element(**kwargs)
        by, value = next(iter(kwargs.items()))
        if self.driver(**kwargs).exists:
            self.driver(**kwargs).click()
            self.log.info('点击元素,method:{}; value:{}'.format(by, value))
        else:
            self.log.error('Something error')
            pass

    def write_element(self, text, **kwargs):
        self.find_element(**kwargs)
        self.driver(**kwargs).set_text(text)

    def find_element(self, **kwargs):
        if not kwargs:
            raise ValueError("Please specify a locator")
        if len(kwargs) > 1:
            raise ValueError("Please specify only one locator")
        by, value = next(iter(kwargs.items()))
        try:
            LOCATOR_LIST[by]
        except KeyError:
            raise ValueError("Element positioning of type '{}' is not supported. ".format(by))










