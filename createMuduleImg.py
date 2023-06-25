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
if __name__ == '__main__':
    originImgPath="./data"
    savePath="./data/fittingModule"
    imgNameList=os.listdir(originImgPath)
    print(imgNameList)
    flag=0
    for i in tqdm(imgNameList):
        try:
            if i.split(".")[1]=="png":
                img=cv2.imread(originImgPath+"/"+i)
                muzzleImg=getMuzzlePart(img)
                gripImg=getGripPart(img)
                stockImg=getStockPart(img)
                cv2.imwrite(savePath+"/muzzle/"+i,muzzleImg)
                cv2.imwrite(savePath+"/grip/"+i,gripImg)
                cv2.imwrite(savePath+"/stock/"+i,stockImg)
                if flag==0:
                    judgeTabImg=getJudgeTabPart(img)
                    cv2.imwrite(originImgPath+"/constant/judgeBag.png",judgeTabImg)
                flag+=1
        except:
            print("非图片，跳过")

