# -*- coding: utf-8 -*-
# author = Administrator
# date = 2020/6/19 16:40

import os
import configparser
from seldom.logging.log import Log

log = Log()


class Config():

    def __init__(self, filepath: str = '/config/config.ini'):
        self.config_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + filepath
        self.conf = configparser.ConfigParser()

    def read_config(self, config_path: str = ''):
        """
        读取配置文件内容
        :param config_path:
        :return:
        """
        if '' == config_path:
            config_path = self.config_path
        return self.conf.read(filenames=config_path, encoding='utf-8')

    def update_config(self, update_data: str, section: str = 'android_test', option: str = 'auto_test_package'):
        """
        更新配置文件内容
        :param update_data:
        :param section:
        :param option:
        :return:
        """
        ini_data = self.get_config_info(section=section, option=option)  # 获取配置文件中对应section下option 值
        if update_data != ini_data:
            log.info('配置文件中测试包名：%s与自动化传入测试包名：%s，更新配置文件的测试包名' % (ini_data, update_data))
            self.conf.set(section=section, option=option, value=update_data)  # 修改配置文件中对应section下option 值
            self.conf.write(open(self.config_path, 'w'))

    def get_config_info(self, section: str, option: str):
        """
        获取配置文件中的[section]下option键对应的值
        :param section:
        :param option:
        :return:
        """
        self.read_config()
        if self.conf.has_option(section=section, option=option):  # 判断配置文件中是否存在对应section, option 值
            ini_data = self.conf.get(section=section, option=option)
            return ini_data
        else:
            raise Exception('config.ini文件中未找到对应的section/option值')


if __name__ == '__main__':
    test = Config()
    test.update_config(update_data='com.kh_super.android.supermerchant')
