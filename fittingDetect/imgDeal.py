import logging
import os
from tqdm import tqdm
import cv2
import pyautogui
from skimage.metrics import structural_similarity
import numpy as np
from config import fittingConfig,globalConfig,personConfig
from fittingDetect.fittingWeights import getFittingWeights
from person import posture
class imageCoper:
    def __init__(self):
        # self.screenWidth,self.screenHeight=pyautogui.size()
        self.screenWidth, self.screenHeight = globalConfig.screenWidth,globalConfig.screenHeight
        self.loadOneFittingModulesByType()
        self.loadCommonModuleByType()
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
    def getBagImg(self):
        screenImg = self.getPic()
        isOpenBagImg=screenImg[int(self.screenHeight * globalConfig.judgeBagBoxYmin):
                            int(self.screenHeight * globalConfig.judgeBagBoxYmax),
                            int(self.screenWidth * globalConfig.judgeBagBoxXmin):
                            int(self.screenWidth * globalConfig.judgeBagBoxXmax)]
        return isOpenBagImg
    def getFittings(self,**kwargs):
        screenImg=self.getPic(**kwargs)
        self.muzzleImg=screenImg[int(self.screenHeight*fittingConfig.muzzleComensator1Ymin):
                            int(self.screenHeight*fittingConfig.muzzleComensator1Ymax),
                            int(self.screenWidth*fittingConfig.muzzleComensator1Xmin):
                            int(self.screenWidth*fittingConfig.muzzleComensator1Xmax)]
        self.gripImg=screenImg[int(self.screenHeight*fittingConfig.grip1Ymin):
                            int(self.screenHeight*fittingConfig.grip1Ymax),
                            int(self.screenWidth*fittingConfig.grip1Xmin):
                            int(self.screenWidth*fittingConfig.grip1Xmax)]
        self.stockImg=screenImg[int(self.screenHeight*fittingConfig.stock1Ymin):
                            int(self.screenHeight*fittingConfig.stock1Ymax),
                            int(self.screenWidth*fittingConfig.stock1Xmin):
                            int(self.screenWidth*fittingConfig.stock1Xmax)]

    @staticmethod
    def compareSimliar(imgGray,moduleImgGray):
        score, diff = structural_similarity(imgGray, moduleImgGray, full=True)
        return score*100
    def loadOneFittingModulesByType(self):
        moduleFittingImgPath = "./data/fittingModule/"
        muzzleFittingPath=moduleFittingImgPath+"muzzle/"
        gripFittingPath=moduleFittingImgPath+"grip/"
        stockFittingPath=moduleFittingImgPath+"stock/"
        muzzleFittingNames=os.listdir(muzzleFittingPath)
        gripFittingNames=os.listdir(gripFittingPath)
        stockFittingNames=os.listdir(stockFittingPath)
        self.muzzleModuleImgDic= {}
        self.gripModuleImgDic={}
        self.stockModuleImgDic={}
        for fitting in tqdm(muzzleFittingNames,unit="img",desc="载入枪口信息"):
            fittingImg=cv2.imread(muzzleFittingPath+fitting)
            self.muzzleModuleImgDic[fitting.split(".")[0]]=fittingImg
        for fitting in tqdm(gripFittingNames,unit="img",desc="载入握把信息"):
            fittingImg=cv2.imread(gripFittingPath+fitting)
            self.gripModuleImgDic[fitting.split(".")[0]]=fittingImg
        for fitting in tqdm(stockFittingNames,unit="img",desc="载入枪托信息"):
            fittingImg=cv2.imread(stockFittingPath+fitting)
            self.stockModuleImgDic[fitting.split(".")[0]]=fittingImg
    def loadCommonModuleByType(self):
        moduleImgPath = "./data/constant/"
        moduleImgname = os.listdir(moduleImgPath)[0]
        moduleImg=cv2.imread(moduleImgPath+moduleImgname)
        self.ifInBagImg = cv2.cvtColor(moduleImg, cv2.COLOR_RGB2GRAY)
        logging.info("载入背包验证模块")

    def classfyOneFitingByType(self,img,fittingType):
        fittingScoredic= {}
        imgGray=cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
        if fittingType=="muzzle":
            for moduleImgName in tqdm(self.muzzleModuleImgDic.keys()):
                moduleImg=self.muzzleModuleImgDic[moduleImgName]
                # ret1,imgThread=cv2.threshold(imgGray,70,255,cv2.THRESH_BINARY)
                # ret1, moduleImgThread = cv2.threshold(moduleImg, 70, 255, cv2.THRESH_BINARY)
                score=self.compareSimliar(imgGray,moduleImg)
                fittingScoredic[moduleImgName]=score
        elif fittingType=="grip":
            for moduleImgName in tqdm(self.gripModuleImgDic.keys()):
                moduleImg=self.gripModuleImgDic[moduleImgName]
                # ret1,imgThread=cv2.threshold(imgGray,70,255,cv2.THRESH_BINARY)
                # ret1, moduleImgThread = cv2.threshold(moduleImg, 70, 255, cv2.THRESH_BINARY)
                score=self.compareSimliar(imgGray,moduleImg)
                fittingScoredic[moduleImgName]=score
        elif fittingType=="stock":
            for moduleImgName in tqdm(self.stockModuleImgDic.keys()):
                moduleImg=self.stockModuleImgDic[moduleImgName]
                # ret1,imgThread=cv2.threshold(imgGray,70,255,cv2.THRESH_BINARY)
                # ret1, moduleImgThread = cv2.threshold(moduleImg, 70, 255, cv2.THRESH_BINARY)
                score=self.compareSimliar(imgGray,moduleImg)
                fittingScoredic[moduleImgName]=score
        fittingScoredic=sorted(fittingScoredic.items(),key=lambda x:x[1],reverse=True)
        if fittingScoredic[0][1]<fittingConfig.fittingDetectTheadShold:
            return "None","None"
        else:
            return fittingScoredic[0][0],fittingScoredic[0][1]

    def classIsInBag(self,img):
        imgGray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        score=imageCoper.compareSimliar(imgGray,self.ifInBagImg)
        if score<personConfig.ifInBagtheadshold:
            return False
        else:
            return True

    def classfyAllFitting(self,**kwargs):
        self.getFittings(**kwargs)
        isOpenBagImg=self.getBagImg()
        ifInbag = self.classIsInBag(isOpenBagImg)
        fittingWeights=1
        if ifInbag:
            logging.info("打开背包")
            muzzleType,muzzleScore=self.classfyOneFitingByType(self.muzzleImg,"muzzle")
            gripType,gripScore=self.classfyOneFitingByType(self.gripImg,"grip")
            stockType,stockScore=self.classfyOneFitingByType(self.stockImg,"stock")
            fittingWeights=getFittingWeights.getWeights(muzzleType,gripType,stockType)
            logging.info("枪口类型为:"+muzzleType+"识别准确率为:"+str(muzzleScore)+"%")
            logging.info("握把类型为:"+gripType+"识别准确率为:"+str(gripScore)+"%")
            logging.info("枪托类型为:"+stockType+"识别准确率为:"+str(stockScore)+"%")
            return fittingWeights
        else:
            logging.info("关闭背包")

