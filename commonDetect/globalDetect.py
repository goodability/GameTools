# -*- coding: utf-8 -*-

'''
@Project ：GameTools 
@File    ：globalDetect.py
@IDE     ：PyCharm 
@Author  ：WeiHao
@Date    ：2023/8/9 22:39 
@Email   ：WeiHao.fox@foxmail.com
'''
import cv2,logging
from commonDetect.baseDetector import BaseDetector
from config import globalConfig,personConfig
class GlobalDetector(BaseDetector):
    def __init__(self):
        super().__init__()
        self.loadCommonModuleByType()
    def loadCommonModuleByType(self):
        moduleImgPath = "./data/constant/"
        moduleBagImgPath = moduleImgPath+"judgeBag.png"
        moduleBagImg=cv2.imread(moduleBagImgPath)
        self.ifInBagImg = cv2.cvtColor(moduleBagImg, cv2.COLOR_RGB2GRAY)
        logging.info("载入背包验证模块")
        moduleMapImgPath=moduleImgPath+"judgeMap.png"
        moduleMapImg=cv2.imread(moduleMapImgPath)
        self.ifOpenMapImg=cv2.cvtColor(moduleMapImg,cv2.COLOR_RGB2GRAY)
        logging.info("载入地图打开判断模块")
    def getBagImg(self,screenImg):
        isOpenBagImg=screenImg[int(self.screenHeight * globalConfig.judgeBagBoxYmin):
                            int(self.screenHeight * globalConfig.judgeBagBoxYmax),
                            int(self.screenWidth * globalConfig.judgeBagBoxXmin):
                            int(self.screenWidth * globalConfig.judgeBagBoxXmax)]
        return isOpenBagImg
    def getMapImg(self):
        screenImg=self.getPic()
        isOpenMapImg=screenImg[int(self.screenHeight * globalConfig.judgeOpenMapYmin):
                            int(self.screenHeight * globalConfig.judgeOpenMapYmax),
                            int(self.screenWidth * globalConfig.judgeOpenMapXmin):
                            int(self.screenWidth * globalConfig.judgeOpenMapXmax)]
        return isOpenMapImg
    def classIsOpenMap(self,img):
        imgGray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        score = self.compareSimliar(imgGray, self.ifOpenMapImg)
        if score < globalConfig.ifOpenMaptheadshold:
            logging.info("关闭地图")
            return False
        else:
            logging.info("打开地图")
            return True
    def classIsInBag(self,img):
        imgGray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        score=self.compareSimliar(imgGray,self.ifInBagImg)
        if score<personConfig.ifInBagtheadshold:
            logging.info("关闭背包")
            return False
        else:
            logging.info("打开背包")
            return True