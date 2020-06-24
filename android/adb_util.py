# -*- coding: utf-8 -*-
# author = Administrator
# date = 2020/6/10 11:29
import os
from seldom.logging.log import Log

log = Log()


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
        log.info('当前测试手机中存在应用，包名：%s' % package_name)
        return True
    else:
        log.warn('当前测试手机未找到应用，包名：%s' % package_name)
        return False


def check_package_process_state(package_name: str):
    """
    校验package_name 对应的包名的进程是否存活
    :param package_name:
    :return:
    """
    script = 'adb shell " ps | grep %s"' % package_name
    if package_name in os_popen(script):
        log.info('当前测试手机中应用进程存活，包名：%s' % package_name)
        return True
    else:
        log.warn('当前测试手机未找到应用进程，包名：%s' % package_name)
        return False


def adb_uninstall(package_name: str):
    """
    通过adb命令卸载指定应用
    :param package_name:包名
    :return:
    """
    script = 'adb uninstall %s' % package_name
    execute_script = os_popen(script)
    if 'Success' in execute_script:
        log.info('卸载应用包名：%s' % package_name)
        return True
    elif 'Unknown package' in execute_script:
        log.warn('未找到卸载应用包名：%s' % package_name)
        return False
    else:
        log.warn('未知异常')
        return False


def adb_install(filepath: str, mode: str):
    """
    通过adb命令安装指定安装包
    :param filepath:安装包文件路径（包括具体的文件名称）
    :return:
    """
    script = 'adb install -r %s' % filepath
    execute_script = os_popen(script)
    if 'Success' in execute_script:
        log.info('安装应用成功，安装包路径：%s' % filepath)
        return True
    elif 'Failure' in execute_script:
        log.warn('安装应用失败，安装包路径：%s' % filepath)
        return False
    else:
        log.warn('未知异常')
        return False


def adb_pull(source_filepath: str, target_filepath: str):
    """
    通过adb命令将移动设备中文件，复制到电脑中的指定路径
    :param source_filepath:
    :param target_filepath:
    :return:
    """
    script = 'adb pull %s %s' % (source_filepath, target_filepath)
    execute_script = os_popen(script)
    if 'pulled' in execute_script:
        log.info('文件 从手机设备拉取到 电脑端 Success，手机设备文件源路径：%s，电脑端存放目标路径：%s'
                 % (source_filepath, target_filepath))
        return True
    else:
        log.warn('文件 从手机设备拉取到电脑端 Failure，手机设备文件源路径：%s，电脑端存放目标路径：%s'
                 % (source_filepath, target_filepath))
        return False


def adb_push(source_filepath: str, target_filepath: str):
    """
    通过adb命令将电脑中文件，推到移动设备中的指定路径
    :param source_filepath:
    :param target_filepath:
    :return:
    """
    script = 'adb push %s %s' % (source_filepath, target_filepath)
    execute_script = os_popen(script)
    if 'pushed' in execute_script:
        log.info('文件 从电脑端推送到 手机设备 Success，电脑端文件源路径：%s，手机设备存放目标路径：%s'
                 % (source_filepath, target_filepath))
        return True
    else:
        log.warn('文件 从电脑端推送到 手机设备 Failure，电脑端文件源路径：%s，手机设备存放目标路径：%s'
                 % (source_filepath, target_filepath))
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
        log.error('截图失败')
        raise Exception('Screen Failure')
    else:
        log.info('截图成功，截图存放目录：/sdcard/screenshot.png')
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
    if 'adb devices' in data or 'adb kill-server' in data or 'adb start-server' in data:
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


def adb_kill_server():
    """
    通过adb命令kill 掉adb server
    :return:
    """
    os_popen('adb kill-server')


def adb_start_server():
    """
    通过adb命令启用 掉adb server
    :return:
    """
    os_popen('adb start-server')


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

