import cv2
import os
import numpy as np
import matplotlib.pyplot as plt
def dealImg(imgPath):
    img=cv2.imread(imgPath)
    grid_RGB=cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    grid_RGB=grid_RGB[:,1520:1900]
    imgsize=(np.shape(grid_RGB)[1],np.shape(grid_RGB)[0])
    grid_HSV = cv2.cvtColor(grid_RGB, cv2.COLOR_RGB2HSV)

    indexList=[]
    # H、S、V范围二：
    lower2 = np.array([156, 43, 46])
    upper2 = np.array([180, 255, 255])
    mask2 = cv2.inRange(grid_HSV, lower2, upper2)
    iimage,contours,_=cv2.findContours(mask2,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    red_points = grid_RGB.copy()
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 0:  # 根据需要设置面积阈值
            cv2.drawContours(red_points, [contour], -1, (0, 0, 255), 2)
            M = cv2.moments(contour)
            if M['m00'] != 0:
                # 计算轮廓的中心坐标
                centroid_x = int(M['m10'] / M['m00'])
                centroid_y = int(M['m01'] / M['m00'])

                # 在图像上绘制轮廓和中心点
                cv2.drawContours(red_points, [contour], -1, (0, 0, 255), 2)
                cv2.circle(red_points, (centroid_x, centroid_y), 5, (0, 0, 255), -1)
                cv2.putText(red_points, f"({centroid_x}, {centroid_y})", (centroid_x + 10, centroid_y + 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                indexList.append([centroid_x,centroid_y])
    # cv2.imshow("Red Points", cv2.resize(red_points,(imgsize[0]//2,imgsize[1]//2)))
    # cv2.imshow("mask",cv2.resize(mask2,(imgsize[0]//2,imgsize[1]//2)))
    # cv2.waitKey()
    step=copeIndex(indexList)
    return step
def copeIndex(indexList):
    sortIndex=sorted(indexList,key=lambda x:x[1],reverse=False)
    step=[]
    for i in range(len(indexList)-1):
        step.append((sortIndex[i][1]-sortIndex[i+1][1])*-1)
    return step[::-1]
def showData(data):
    fig, (ax1, ax2) = plt.subplots(1, 2)
    fig.set_size_inches(20, 8)
    ace_base=1
    m762_base=1
    ace_median=1
    m762_median=1
    for i in data.keys():
        if i.startswith("ace"):
            # plt.subplot(2,1,1)
            ax1.plot(data[i],label=i,marker="o")
        elif i.startswith("m762"):
            # plt.subplot(2, 1, 2)
            ax2.plot(data[i],label=i,marker="s")
        if i=="ace_none":
            ace_base=np.mean(data[i])
            ace_median=np.median(data[i])
        if i=="m762_none":
            m762_base=np.mean(data[i])
            m762_median=np.median(data[i])
    for i in data.keys():
        if i.startswith("ace"):
            print(data[i],i," meanL :",np.mean(data[i]),"比率： ",np.mean(data[i])/ace_base,"中位数比率 ：",np.median(data[i])/ace_median)
        if i.startswith("m762"):
            print(data[i], i, " meanL :", np.mean(data[i]), "比率： ", np.mean(data[i]) /m762_base,"中位数比率 ：",np.median(data[i])/m762_median)
    ax1.legend()
    ax2.legend()
    plt.show()
def run(filePath):
    imgList=os.listdir(filePath)
    result={}
    for i in  imgList:
        imgname=i.split(".")[0]
        step=dealImg(filePath+"/"+i)
        result[imgname]=step
    showData(result)
# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':
    imgPath="../data/mulitiGunDataTest"
    run(imgPath)

