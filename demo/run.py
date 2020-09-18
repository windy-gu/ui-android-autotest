import seldom

if __name__ == '__main__':
    # seldom.main(path="./test_dir",
    #             browser="firefox",
    #             title="百度测试用例",
    #             description="测试环境：Firefox",
    #             rerun=0)
    seldom.main(test_type='android', test_package='com.kh_super.android.supermerchant', path="./test_dir", debug=False,
                rerun=1, title='Merchant Test Report', description='测试执行情况如下所示')

'''
说明：
test_type ： 测试类型android/web
test_package ： 测试包名，用于校验测试设备是否安装对应的应用，进程是否存活
path ： 指定测试目录。
browser: 指定浏览，默认chrome。
report：日志报告文件名称&格式，若为空，则默认report+时间+.html，并且在当前生成reports文件夹
title ： 指定测试报告中标题。默认：Seldom Test Report
description ： 指定测试报告中环境描述。默认：Test case execution
debug ： debug模式，设置为True不生成HTML测试报告。
rerun ： 测试失败重跑次数，默认为0
save_last_run：默认为False，若为True，则只保存最后一次运行的结果
driver_path：默认为None，指定浏览器驱动路径
param grid_url：指定远程执行用例ip地址

'''

