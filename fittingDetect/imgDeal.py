import logging
import os
from tqdm import tqdm
import cv2
import pyautogui
from skimage.metrics import structural_similarity
import numpy as np
from config import fittingConfig
class imageCoper:
    def __init__(self):
        self.screenWidth,self.screenHeight=pyautogui.size()
        # self.screenWidth, self.screenHeight = 2560,1440
    def getPic(self,**kwargs):
        if "img" in kwargs.keys():
            return kwargs["img"]
        img=pyautogui.screenshot()
        img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        return img
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
        # cv2.imshow("compen",self.muzzleImg)
        # cv2.imshow("grip",self.gripImg)
        # cv2.imshow("stock",self.stockImg)
        # cv2.waitKey(0)
    def compareSimliar(self,imgGray,moduleImgGray):
        score, diff = structural_similarity(imgGray, moduleImgGray, full=True)
        return score*100
    def classfyOneFitingByType(self,img,fittingType):
        moduleFittingImgPath="./data/fittingModule/"+fittingType
        oneFittingModules=os.listdir(moduleFittingImgPath)
        fittingScoredic= {}
        imgGray=cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
        for moduleFitting in tqdm(oneFittingModules):
            moduleImg=cv2.imread(moduleFittingImgPath+"/"+moduleFitting)
            moduleImgGray=cv2.cvtColor(moduleImg,cv2.COLOR_RGB2GRAY)
            moduleImgGray=cv2.resize(moduleImgGray,(img.shape[1],img.shape[0]))
            ret1,imgThread=cv2.threshold(imgGray,70,255,cv2.THRESH_BINARY)
            ret1, moduleImgThread = cv2.threshold(moduleImgGray, 70, 255, cv2.THRESH_BINARY)
            score=self.compareSimliar(imgGray,moduleImgGray)
            fittingScoredic[moduleFitting.split(".")[0]]=score
        fittingScoredic=sorted(fittingScoredic.items(),key=lambda x:x[1],reverse=True)
        if fittingScoredic[0][1]<40:
            return "None","None"
        else:
            return fittingScoredic[0][0],fittingScoredic[0][1]
        pass
    def classfyAllFitting(self,**kwargs):
        self.getFittings(**kwargs)
        muzzleType,muzzleScore=self.classfyOneFitingByType(self.muzzleImg,"compensator")
        gripType,gripScore=self.classfyOneFitingByType(self.gripImg,"grip")
        stockType,stockScore=self.classfyOneFitingByType(self.stockImg,"stock")
        logging.info("枪口类型为:"+muzzleType+"识别准确率为:"+str(muzzleScore)+"%")
        logging.info("握把类型为:"+gripType+"识别准确率为:"+str(gripScore)+"%")
        logging.info("枪托类型为:"+stockType+"识别准确率为:"+str(stockScore)+"%")

            # imgGray=cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
            # moduleImgGray=cv2.cvtColor(moduleImg,cv2.COLOR_RGB2GRAY)
            # moduleImgGray=cv2.resize(moduleImgGray,(imgGray.shape[1],imgGray.shape[0]))
            # ret,thread1=cv2.threshold(imgGray,70,255,cv2.THRESH_BINARY)
            # ret,thread2=cv2.threshold(moduleImgGray,70,255,cv2.THRESH_BINARY)
            # score, diff = structural_similarity(thread1, thread2, full=True)
            # score1,diff1=structural_similarity(imgGray, moduleImgGray, full=True)
            # print("Similarity Score: {:.3f}%".format(score * 100))
            # print("Similarity Score gray: {:.3f}%".format(score1 * 100))