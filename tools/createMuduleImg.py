import os
import cv2
from tqdm import tqdm
from config import fittingConfig,globalConfig,gunConfig

def getMuzzlePart(img):
    muzzleImg = img[int(globalConfig.screenHeight * fittingConfig.muzzleComensator1Ymin):
                          int(globalConfig.screenHeight * fittingConfig.muzzleComensator1Ymax),
                int(globalConfig.screenWidth * fittingConfig.muzzleComensator1Xmin):
                int(globalConfig.screenWidth * fittingConfig.muzzleComensator1Xmax)]
    return muzzleImg
def getGripPart(img):
    gripImg = img[int(globalConfig.screenHeight * fittingConfig.grip1Ymin):
                        int(globalConfig.screenHeight * fittingConfig.grip1Ymax),
              int(globalConfig.screenWidth * fittingConfig.grip1Xmin):
              int(globalConfig.screenWidth * fittingConfig.grip1Xmax)]
    return gripImg
def getStockPart(img):
    stockImg = img[int(globalConfig.screenHeight * fittingConfig.stock1Ymin):
                         int(globalConfig.screenHeight * fittingConfig.stock1Ymax),
               int(globalConfig.screenWidth * fittingConfig.stock1Xmin):
               int(globalConfig.screenWidth * fittingConfig.stock1Xmax)]
    return stockImg
def getJudgeTabPart(img):
    isTabImg=img[int(globalConfig.screenHeight * globalConfig.judgeBagBoxYmin):
                int(globalConfig.screenHeight * globalConfig.judgeBagBoxYmax),
               int(globalConfig.screenWidth * globalConfig.judgeBagBoxXmin):
               int(globalConfig.screenWidth * globalConfig.judgeBagBoxXmax)]
    return isTabImg
def getJudgeMapPart(img):
    isMapImg=img[int(globalConfig.screenHeight * globalConfig.judgeOpenMapYmin):
                int(globalConfig.screenHeight * globalConfig.judgeOpenMapYmax),
               int(globalConfig.screenWidth * globalConfig.judgeOpenMapXmin):
               int(globalConfig.screenWidth * globalConfig.judgeOpenMapXmax)]
    return isMapImg
def getGunPostionPart(img):
    gunNameImg=img[int(globalConfig.screenHeight * gunConfig.gunPostionYmin):
                int(globalConfig.screenHeight * gunConfig.gunPostionYmax),
               int(globalConfig.screenWidth * gunConfig.gunPostionXmin):
               int(globalConfig.screenWidth * gunConfig.gunPostionXmax)]
    return gunNameImg
def createFittingPart(originImgPath,savePath):
    for typeDir in originImgPath:
        fittingType=typeDir.split("\\")[-1]
        print("create type:",fittingType)
        fittingTypeList=os.listdir(typeDir)
        for r in fittingTypeList:
            img=cv2.imread(typeDir+"/"+r)
            if fittingType=="muzzle":
                muzzleImg=getMuzzlePart(img)
                cv2.imwrite(savePath+"/muzzle/"+r,muzzleImg)
            elif fittingType=="grip":
                gripImg=getGripPart(img)
                cv2.imwrite(savePath+"/grip/"+r,gripImg)
            elif fittingType=="stock":
                stockImg=getStockPart(img)
                cv2.imwrite(savePath+"/stock/"+r,stockImg)
def createBagBoxPart(oriPath,savePath):
        img = cv2.imread(oriPath)
        bagBoxImg=getJudgeTabPart(img)
        grayImg = cv2.cvtColor(bagBoxImg, cv2.COLOR_BGR2GRAY)
        # 再将图片变为黑白图片（灰度值大于127的重置像素值为255，否则重置像素值为0，也就是通过阈值127将图像二值化-要么黑要么白）
        ret, thresh = cv2.threshold(grayImg, 150, 255, cv2.THRESH_BINARY)
        cv2.imwrite(savePath+"/constant/judgeBag.png",thresh)
def createMapPart(oriPath,savePath):
    img=cv2.imread(oriPath)
    isOpenMapImg=getJudgeMapPart(img)
    grayImg = cv2.cvtColor(isOpenMapImg, cv2.COLOR_BGR2GRAY)
    # 再将图片变为黑白图片（灰度值大于127的重置像素值为255，否则重置像素值为0，也就是通过阈值127将图像二值化-要么黑要么白）
    ret, thresh = cv2.threshold(grayImg, 150, 255, cv2.THRESH_BINARY)
    cv2.imwrite(savePath+"/constant/judgeMap.png",thresh)
    print("成功构建判断是否打开地图模板")
def createGunTypeModule(oriPath,savePath):
    gunList=os.listdir(oriPath)
    print(gunList)
    for r,path in enumerate(gunList):
        img=cv2.imread(oriPath+"/"+path)
        gunNameImg=getGunPostionPart(img)
        grayImg = cv2.cvtColor(gunNameImg, cv2.COLOR_BGR2GRAY)
        # 再将图片变为黑白图片（灰度值大于127的重置像素值为255，否则重置像素值为0，也就是通过阈值127将图像二值化-要么黑要么白）
        ret, thresh = cv2.threshold(grayImg, 200, 255, cv2.THRESH_BINARY)
        cv2.imwrite(savePath+"\\"+path,thresh)
        print(savePath+"\\"+path)
if __name__ == '__main__':
    # fittingOriginImgPath=[r"E:\temp\muzzle",r"E:\temp\grip",r"E:\temp\stock"]
    bagPath=r"E:\temp\constant\bag.png"
    # mapPath=r"E:\temp\constant\map.png"
    savePath="../data"
    # imgNameList=os.listdir(originImgPath)
    # createFittingPart(fittingOriginImgPath,savePath)
    # createBagBoxPart(bagPath,savePath)
    # createMapPart(mapPath,savePath)
    # createGunTypeModule(originImgPath,savePath)
