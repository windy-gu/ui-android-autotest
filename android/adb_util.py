# -*- coding: utf-8 -*-
# author = Administrator
# date = 2020/6/10 11:29
import os


def os_popen(data: str, type: str = 'read'):
    """
    命令行中执行adb等语句，并返回对应的执行结果
    :param data:
    :param type:
    :return:
    """
    if '' == data:
        return False
    else:
        if '\\' in data:
            data = data.replace('\\', '/')
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
    script = 'adb shell "pm list package -3 | grep %s"' % package_name
    if package_name in os_popen(script):
        return True
    else:
        return False


def check_package_process_state(package_name: str):
    """
    校验package_name 对应的包名的进程是否存活
    :param package_name:
    :return:
    """
    script = 'adb shell " ps | grep %s"' % package_name
    if package_name in os_popen(script):
        return True
    else:
        return False


def adb_uninstall(package_name: str):
    """
    通过adb命令卸载指定安装包
    :param package_name:
    :return:
    """
    script = 'adb uninstall %s' % package_name
    execute_script = os_popen(script)
    if 'Success' in execute_script:
        return True
    elif 'Unknown package' in execute_script:
        return False
    else:
        return False


def adb_install(filepath: str):
    """

    :param filepath:
    :return:
    """
    script = 'adb install %s' % filepath
    execute_script = os_popen(script)
    if 'Success' in execute_script:
        return True
    elif 'Failure' in execute_script:
        return False
    else:
        return False


def adb_pull(source_filepath: str, target_filepath: str):
    """

    :param source_filepath:
    :param target_filepath:
    :return:
    """
    script = 'adb pull %s %s' % (source_filepath, target_filepath)
    execute_script = os_popen(script)
    if 'pulled' in execute_script:
        return True
    else:
        return False


def adb_push(source_filepath: str, target_filepath: str):
    """

    :param source_filepath:
    :param target_filepath:
    :return:
    """
    script = 'adb push %s %s' % (source_filepath, target_filepath)
    execute_script = os_popen(script)
    if 'pushed' in execute_script:
        return True
    else:
        return False


def adb_screencap(target_filepath: str):
    """
    默认在手机设备中 /sdcard/screenshot.png
    :param target_filepath:
    :return:
    """
    script_screencap = 'adb shell /system/bin/screencap -p /sdcard/screenshot.png'
    execute_script_screencap = os_popen(script_screencap)
    if 'not found' in execute_script_screencap:
        raise Exception('Screen Failure')
    screen_filepath = '/sdcard/screenshot.png'
    script_push_state = adb_push(screen_filepath, target_filepath)
    if script_push_state:
        return True
    else:
        return False


def adb_screenrecord(target_filepath: str):
    """

    :param target_filepath:
    :return:
    """
    pass


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


def adb_screen_state():
    """
    通过adb命令获取手机屏幕的状态信息
    :return:
    """
    data = os_popen('adb shell dumpsys window policy|find "screenState"').strip()  # strip()去除首位空格
    return data


def adb_phone_brand():
    """
    通过adb命令获取手机品牌信息
    :return:
    """
    brand = os_popen('adb shell getprop ro.product.brand').strip()
    return brand


def adb_phone_model():
    """
    通过adb命令获取手机型号信息
    :return:
    """
    model = os_popen('adb  shell getprop ro.product.model').strip()
    return model


def adb_phone_android_version():
    """
    通过adb命令获取手机-android 系统版本
    :return:
    """
    version = os_popen('adb shell getprop ro.build.version.release').strip()
    return version


def adb_phone_resolution():
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


def adb_phone_info():
    """
    通过adb命令获取手机相关信息
    :return:
    """
    info = os_popen('adb  shell "getprop | grep product"').strip().replace('[', '').replace(']', '')
    return info


def adb_phone_imei():
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
    print(adb_install('C:\\Users\\Administrator\\Downloads\\0b1214b56924b106bbf0ceef30b570db.apk'))
    # print(check_package_process_state('com.kh_super.android.supermerchant'))

