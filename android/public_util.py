# -*- coding: utf-8 -*-
# author = Administrator
# date = 2020/6/19 16:40

import os
import configparser
from seldom.logging.log import Log

log = Log()


class Config():

    def __init__(self, filepath: str = '\\config\\config.ini'):
        self.config_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + filepath
        self.conf = configparser.ConfigParser()

    def read_config(self, config_path: str = ''):
        if '' == config_path:
            config_path = self.config_path
        return self.conf.read(filenames=config_path, encoding='utf-8')

    def update_config(self, update_data: str, section: str = 'android_test', option: str = 'auto_test_package'):
        # self.read_config()
        ini_data = self.get_config_info(section=section, option=option)  # 获取配置文件中对应section下option 值
        if update_data != ini_data:
            self.conf.set(section=section, option=option, value=update_data)  # 修改配置文件中对应section下option 值
            self.conf.write(open(self.config_path, 'w'))

    def get_config_info(self, section: str, option: str):
        self.read_config()
        if self.conf.has_option(section=section, option=option):  # 判断配置文件中是否存在对应section, option 值
            ini_data = self.conf.get(section=section, option=option)
            return ini_data
        else:
            raise Exception('config.ini文件中未找到对应的section/option值')


if __name__ == '__main__':
    test = Config()

    test.update_config(update_data='com.kh_super.android.supermerchant')