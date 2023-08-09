import os
import cv2
from tqdm import tqdm
from config import fittingConfig,globalConfig

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
def createFittingPart(originImgPath,savePath):
    imgNameList = os.listdir(originImgPath)
    print(imgNameList)
    for i in tqdm(imgNameList):
        try:
            if i.split(".")[1] == "png":
                img = cv2.imread(originImgPath + "/" + i)
                muzzleImg = getMuzzlePart(img)
                gripImg = getGripPart(img)
                stockImg = getStockPart(img)
                cv2.imwrite(savePath + "/fittingModule/muzzle/" + i, muzzleImg)
                cv2.imwrite(savePath + "/fittingModule/grip/" + i, gripImg)
                cv2.imwrite(savePath + "/fittingModule/stock/" + i, stockImg)
        except:
            print("非图片，跳过")
def createBagBoxPart(oriPath,savePath):
    fileList=os.listdir(oriPath)
    for i in fileList:
        if i.split(".")[1]=="png":
            img = cv2.imread(originImgPath + "/" + i)
            bagBoxImg=getJudgeTabPart(img)
            cv2.imwrite(savePath+"/constant/judgeBag.png",bagBoxImg)
            break
def createMapPart(oriPath,savePath):
    imgPath=oriPath+"/constant/map.png"
    img=cv2.imread(imgPath)
    isOpenMapImg=getJudgeMapPart(img)
    cv2.imwrite(savePath+"/constant/judgeMap.png",isOpenMapImg)
    print("成功构建判断是否打开地图模板")
if __name__ == '__main__':
    originImgPath="./data"
    savePath="./data"
    imgNameList=os.listdir(originImgPath)
    createFittingPart(originImgPath,savePath)
    createBagBoxPart(originImgPath,savePath)
    createMapPart(originImgPath,savePath)
