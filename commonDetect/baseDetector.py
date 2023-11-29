# -*- coding: utf-8 -*-

'''
@Project ：GameTools 
@File    ：baseDetector.py
@IDE     ：PyCharm 
@Author  ：WeiHao
@Date    ：2023/8/9 22:45 
@Email   ：WeiHao.fox@foxmail.com
'''
from config import globalConfig
from config.log import logging
import cv2,pyautogui
import numpy as np
from skimage.metrics import structural_similarity
class BaseDetector:
    def __init__(self):
        # self.screenWidth,self.screenHeight=pyautogui.size()
        self.screenWidth, self.screenHeight = globalConfig.screenWidth,globalConfig.screenHeight
    def getPic(self,**kwargs):
        if "img" in kwargs.keys():
            return kwargs["img"]
        img=pyautogui.screenshot()
        img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        img=self.adaptAllScreen(img)
        return img
    def adaptAllScreen(self,img):
        if self.screenWidth!=globalConfig.screenWidth or self.screenHeight!=globalConfig.screenHeight:
            img=cv2.resize(img,(globalConfig.screenWidth,globalConfig.screenHeight))
        return img
    @staticmethod
    def compareSimliar(imgGray,moduleImgGray):
        score, diff = structural_similarity(imgGray, moduleImgGray, full=True)
        return score*100