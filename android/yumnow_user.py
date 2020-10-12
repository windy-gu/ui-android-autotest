# -*- coding: utf-8 -*-
# author = Administrator
# date = 2020/9/24 16:52
import cx_Oracle
import random
import csv


def get_phone_number_cambodia(check: bool = False):
    """随机生成855可用运营商号段号码
    """
    phone_list = ['11', '12', '14', '17', '61', '76', '77', '78', '79', '85', '89', '92',
                  '95', '99', '10', '15', '16', '69', '70', '81', '86', '87', '93',
                  '96', '98', '31', '60', '66', '67', '68', '71', '88', '90', '97',
                  '13', '80', '83', '84', '38', '18'
                  ]  # 柬埔寨可正常使用手机号号段
    phone_seven_long = ['76', '96', '31', '71', '88', '97', '38', '18']
    phone_segment = random.choice(phone_list)
    if phone_segment == '12':
        num_length = random.randint(6, 7)
    elif phone_segment in phone_seven_long:
        num_length = random.randint(7, 7)
    else:
        num_length = random.randint(6, 6)

    register_number = '8550' + phone_segment + "".join(random.choice("0123456789") for i in range(num_length))

    # 判断是否需要校验号码已注册，校验会严重降低速度
    if check:
        check_oracle = Oracle(username='lifekh_mp_customer', password='djk876KKJJhyyhg787654J',
                              address='172.17.2.240:1521/lifekh')
        check_data = check_oracle.select_all('SELECT LOGIN_NAME from "LIFEKH_MP_CUSTOMER"."USER_OPERATOR_LOGIN_INFO" WHERE "LOGIN_NAME" =' + "'%s'" % register_number)
        if len(check_data) != 0:
            if register_number in ''.join(check_data[0]):
                print('%s 账号已注册' % register_number)
                get_phone_number_cambodia()
        else:
            print('%s 可正常使用' % register_number)
    return register_number


def write_csv(file: str, times=1):
    with open(file, newline='', encoding='utf-8', mode='w') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(['loginName'])
        for i in range(0, times):
            login_no = get_phone_number_cambodia()
            csv_writer.writerow([login_no])


class Oracle:
    def __init__(self, username: str, password: str, address: str):
        self.username = username
        self.password = password
        self.address = address

    def select_all(self, expression: str):
        db = cx_Oracle.connect(self.username, self.password, self.address)
        cur = db.cursor()
        cur.execute(expression)
        rows = cur.fetchall()
        cur.close()
        db.close()
        return rows


class MySQL:
    def __init__(self, username: str, password: str, address: str):
        self.username = username
        self.password = password
        self.address = address


if __name__ == '__main__':
    # get_phone_number_cambodia()
    # oracle = Oracle(username='lifekh_mp_customer', password='djk876KKJJhyyhg787654J', address='172.17.2.240:1521/lifekh')
    # select_data = oracle.select_all('SELECT LOGIN_NAME from "LIFEKH_MP_CUSTOMER"."USER_OPERATOR_LOGIN_INFO" WHERE "LOGIN_NAME" =' + "'85510147261'")
    # print(select_data)
    # print(type(select_data))
    # # result =
    # if '85510147261' in ''.join(select_data[0]):
    #     print('Yes')
    # else:
    #     print('No')
    write_csv('C:\\Users\Administrator\\Desktop\\jmeter script\\chaoA_performance_test\\test_data\\performance_register_loginName.csv', times=2000)




