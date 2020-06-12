# -*- coding: utf-8 -*-
# author = Administrator
# date = 2020/6/10 11:29
import os


def os_popen(data: str, type: str='read'):
    """
    命令行中执行adb等语句，并返回对应的执行结果
    :param data:
    :return:
    """
    if '' == data:
        pass
    else:
        if 'adb' in data:
            data = adb_add_serial_number(data)
        with os.popen(data, 'r') as p:
            if type == 'read':
                r = p.read()
            elif type == 'readlines':
                r = p.readlines()
    return r


def check_package_install_state(package_name: str):
    """
    校验package_name 对应的包名是否存在在当前设备测试设备中
    :param package_name: 包名
    :return:
    """
    check_package = 'adb shell "pm list package -3 | grep %s"' % package_name
    if package_name in os_popen(check_package):
        return True
    else:
        return False


def adb_add_serial_number(data: str):
    """
    给所有的adb 查询语句添加 -s serial_number
    :param data: adb查询语句
    :return:
    """
    if 'adb devices' in data:
        return data
    split_data = data.split(' ', 1)
    serial_number = ' -s '+os.popen('adb devices').read().split('\n')[1].split('\t')[0] + ' '
    if ' -s  ' == serial_number:
        raise Exception('adb devices未检测到android设备')
    else:
        res = split_data[0] + serial_number + split_data[1]
    return res


def screen_state():
    """
    通过adb命令获取手机屏幕的状态信息
    :return:
    """
    data = os_popen('adb shell dumpsys window policy|find "screenState"').strip()
    return data


def phone_brand():
    """
    通过adb命令获取手机品牌信息
    :return:
    """
    brand = os_popen('adb shell getprop ro.product.brand').strip()
    return brand


def phone_model():
    """
    通过adb命令获取手机型号信息
    :return:
    """
    model = os_popen('adb  shell getprop ro.product.model').strip()
    return model


def phone_android_version():
    """
    通过adb命令获取手机-android 系统版本
    :return:
    """
    version = os_popen('adb shell getprop ro.build.version.release').strip()
    return version


def phone_resolution():
    """
    通过adb命令获取手机分辨率
    :return:
    """
    resolution = ''
    data = os_popen(data='adb  shell wm size', type='readlines')
    for n in data:
        if 'Physical' in n:
            resolution = n.split(':')[1].strip()
            break
    return resolution


def phone_info():
    """
    通过adb命令获取手机相关信息
    :return:
    """
    info = os_popen('adb  shell "getprop | grep product"').strip().replace('[', '').replace(']', '')
    return info


def phone_imei():
    """
    通过adb命令获取手机imei信息
    :return:
    """
    imei = ''
    data = os_popen(data='adb shell service call iphonesubinfo 1', type='readlines')
    for n in data:
        if 'Result' in n:
            continue
        else:
            imei = imei + n.strip().split("'")[1]
    imei = imei.replace('.', '').strip()
    return imei


if __name__ == '__main__':
    print(phone_brand())
    print(phone_model())
    print(phone_imei())
    # print(phone_serial_number())
    print(phone_android_version())
    print(phone_resolution())
