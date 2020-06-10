# -*- coding: utf-8 -*-
# author = Administrator
# date = 2020/6/10 11:29
import os


def os_popen(data: str):
    if '' == data:
        pass
    else:
        with os.popen(data, 'r') as p:
            r = p.read()
    return r
