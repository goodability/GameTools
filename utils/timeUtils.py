# -*- coding: utf-8 -*-

'''
@Project ：GameTools 
@File    ：timeUtils.py
@IDE     ：PyCharm 
@Author  ：WeiHao
@Date    ：2023/8/25 11:35 
@Email   ：WeiHao.fox@foxmail.com
'''
import time


class Timer:
    def __init__(self):
        pass
    @staticmethod
    def sleep(sleepTime):
        timeStart=time.perf_counter()
        while True:
            timeEnd=time.perf_counter()
            if(timeEnd-timeStart>=sleepTime):
                # print("实际睡眠时间",(timeEnd-timeStart)*1000,"期望睡眠时间",sleepTime*1000)
                break
