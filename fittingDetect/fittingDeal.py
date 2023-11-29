from config.log import logging
import os
from tqdm import tqdm
import cv2
from config import fittingConfig,globalConfig,personConfig,gunConfig
from fittingDetect.fittingWeights import getFittingWeights
from person import posture
from commonDetect.baseDetector import BaseDetector
from commonDetect.globalDetect import GlobalDetector
class imageCoper(BaseDetector):
    def __init__(self):
        super().__init__()
        self.loadFittingModulesByType()
        self.loadGunsModule()
        self.globalDetector=GlobalDetector()

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
        self.gunNameImg=screenImg[int(self.screenHeight*gunConfig.gunPostionYmin):
                            int(self.screenHeight*gunConfig.gunPostionYmax),
                            int(self.screenWidth*gunConfig.gunPostionXmin):
                            int(self.screenWidth*gunConfig.gunPostionXmax)]
    def loadFittingModulesByType(self):
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
            fittingImgGray=cv2.cvtColor(fittingImg, cv2.COLOR_RGB2GRAY)
            self.muzzleModuleImgDic[fitting.split(".")[0]]=fittingImgGray
        for fitting in tqdm(gripFittingNames,unit="img",desc="载入握把信息"):
            fittingImg=cv2.imread(gripFittingPath+fitting)
            fittingImgGray = cv2.cvtColor(fittingImg, cv2.COLOR_RGB2GRAY)
            self.gripModuleImgDic[fitting.split(".")[0]]=fittingImgGray
        for fitting in tqdm(stockFittingNames,unit="img",desc="载入枪托信息"):
            fittingImg=cv2.imread(stockFittingPath+fitting)
            fittingImgGray = cv2.cvtColor(fittingImg, cv2.COLOR_RGB2GRAY)
            self.stockModuleImgDic[fitting.split(".")[0]]=fittingImgGray
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
    def loadGunsModule(self):
        gunModuleImgPath="./data/gunTypeModules"
        gunNamesList=os.listdir(gunModuleImgPath)
        self.gunModuleImgsDic={}
        for gunImgName in tqdm(gunNamesList,unit="img",desc="载入枪械类型"):
            thisGunName=gunImgName.split(".")[0]
            thisGunImg=cv2.imread(gunModuleImgPath+"/"+gunImgName)
            thisGunImgGray=cv2.cvtColor(thisGunImg,cv2.COLOR_RGB2GRAY)
            self.gunModuleImgsDic[thisGunName]=thisGunImgGray
    def getGunNameImg(self,screenImg):
        thisGunNameImg = screenImg[int(self.screenHeight * gunConfig.gunPostionYmin):
                                 int(self.screenHeight * gunConfig.gunPostionYmax),
                       int(self.screenWidth * gunConfig.gunPostionXmin):
                       int(self.screenWidth * gunConfig.gunPostionXmax)]
        return thisGunNameImg
    def classfyGun(self,thisGunNameImg):
        gunSocreDic={}
        thisGunImgGray=cv2.cvtColor(thisGunNameImg,cv2.COLOR_RGB2GRAY)
        for moduleImgName in tqdm(self.gunModuleImgsDic.keys()):
            moduleImgGray=self.gunModuleImgsDic[moduleImgName]
            score=self.compareSimliar(thisGunImgGray,moduleImgGray)
            gunSocreDic[moduleImgName]=score
        gunSocreDic= sorted(gunSocreDic.items(), key=lambda x: x[1], reverse=True)
        if gunSocreDic[0][1] < gunConfig.gunTypeThreashold:
            return "None", "None"
        else:
            return gunSocreDic[0][0], gunSocreDic[0][1]

    def classfyAllFitting(self,**kwargs):
        self.getFittings(**kwargs)
        fittingWeights=1
        muzzleType,muzzleScore=self.classfyOneFitingByType(self.muzzleImg,"muzzle")
        gripType,gripScore=self.classfyOneFitingByType(self.gripImg,"grip")
        stockType,stockScore=self.classfyOneFitingByType(self.stockImg,"stock")
        gunType,gunScore=self.classfyGun(self.gunNameImg)
        logging.info("枪械为:"+gunType+"识别准确率为:"+str(gunScore)+"%")
        fittingWeights = getFittingWeights.getWeights(gunType, muzzleType, gripType, stockType)
        logging.info("枪口类型为:" + muzzleType + "识别准确率为:" + str(muzzleScore) + "%")
        logging.info("握把类型为:" + gripType + "识别准确率为:" + str(gripScore) + "%")
        logging.info("枪托类型为:" + stockType + "识别准确率为:" + str(stockScore) + "%")
        return fittingWeights,gunType

