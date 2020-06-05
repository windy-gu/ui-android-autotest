# -*- coding: utf-8 -*-
# author = Administrator
# date = 2020/6/2 10:46
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
    # driver = None
    # log = Log()

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










