import time,sys
from GUI import app
import pyautogui
import win32api
from utils.timeUtils import Timer
import win_precise_time as wpt
import numpy as np
from person import posture
from pynput.keyboard import Key
from config.log import logging
from config import gunConfig,globalConfig,personConfig
from pynput import keyboard,mouse
from pynput.mouse import Controller
from threadPool import ThreadPool
import pydirectinput
from fittingDetect.fittingDeal import imageCoper
from commonDetect.globalDetect import GlobalDetector
STATUS=-1
fittingWeights=1
isSquat=False
isGrovel=False
holdKeyFlag=False
isHoldBreath=False
is_left_button_pressed=False
ifInBag=False
ifOpenMap=False
is_open_mirror=False#按下鼠标右键代表按下右键
right_button_press_time=0
right_button_release_time=0
imgcoper=imageCoper()
globalDetector=GlobalDetector()
def on_press(key):
    global STATUS,gun,isSquat,isGrovel,isHoldBreath,fittingWeights,is_open_mirror,ifInBag,ifOpenMap
    # try:
    if key==Key.caps_lock:
        STATUS=STATUS*-1
        if STATUS==1:
            logging.info("开关打开！")
        else:
            logging.info("开关关闭！")
    #开关打开才能选择枪械
    if STATUS==1:
        # print(key),type(key)
        #识别配件
        if key==Key.tab:
            time.sleep(0.03)
            screenImg=globalDetector.getPic()
            BagImg = globalDetector.getBagImg(screenImg)
            ifInBag = globalDetector.classIsInBag(BagImg)
            if ifInBag:
                fittingActualWeights,gun=imgcoper.classfyAllFitting(img=screenImg)
                if fittingActualWeights is not None:
                    fittingWeights=fittingActualWeights
            #按了tab会自动关闭瞄准镜
            is_open_mirror=False
        #换弹会自动关闭瞄准镜
        elif str(key)=="'r'" or str(key)=="'R'":
            is_open_mirror=False
        #蹲下
        elif str(key)=="'c'" or str(key)=="'C'":
            if isSquat==False:
                isSquat=True
                isGrovel=False
            else:
                isSquat=False
        #趴下
        elif str(key)=="'z'" or str(key)=="'Z'":
            if isGrovel==False:
                isGrovel=True
                isSquat=False
            else:
                isGrovel=False
        #打开地图
        elif str(key)=="'m'" or str(key)=="'M'":
            time.sleep(0.03)
            mapImg=globalDetector.getMapImg()
            ifOpenMap=globalDetector.classIsOpenMap(mapImg)
            #如果检测到打开地图了，就直接暂时关掉开关，也就相当于屏蔽掉鼠标按键和键盘按键
        #按下空格姿态会变成直立
        elif key==Key.space:
            isGrovel=False
            isSquat=False
        #屏息
        elif key==Key.shift and isHoldBreath==False:
            isHoldBreath=True
        #重置人物姿态，站立，不屏息
        elif key==Key.enter:
            [isGrovel,isHoldBreath,isSquat,is_open_mirror]=\
                posture.resetPosture(isGrovel,isHoldBreath,isSquat,is_open_mirror)
            logging.info("重置人物姿态")
    # except:
    #     logging.error("未知错误...")
def on_release(key):
    global isHoldBreath
    if key==Key.shift:
        isHoldBreath=False
def on_click(x,y,button,pressed):
    if STATUS==1:
        global is_left_button_pressed,is_open_mirror,ifInBag,ifOpenMap,right_button_press_time,right_button_release_time
        if button == mouse.Button.left:
            is_left_button_pressed = pressed
            if pressed and is_open_mirror and not ifInBag and not ifOpenMap:
                ThreadPool.pool.submit(moveMouse)
        elif button==mouse.Button.right:
            if not ifInBag and not ifOpenMap:
                if pressed==True:
                    right_button_press_time=time.perf_counter()
                else:
                    right_button_release_time=time.perf_counter()
                    if is_open_mirror==False:
                        holdTime=(right_button_release_time-right_button_press_time)*1000
                        if holdTime<personConfig.ifNoMirrorShoot:
                            is_open_mirror=True
                    else:
                        is_open_mirror=False


def getGunData():
    global gun,isSquat,isGrovel,isHoldBreath,fittingWeights
    gunStep=gunConfig.guns[gun]["basic"]
    shootRate=gunConfig.guns[gun]["speed"]
    stepWeight=posture.getPostureWeight(isGrovel,isHoldBreath,isSquat,gun)
    logging.info("开枪姿态后座控制权重"+str(stepWeight)+"---配件后座控制权重"+str(fittingWeights))
    gun_step=np.array(gunStep)*stepWeight*fittingWeights
    gun_step=gun_step/globalConfig.vertical
    return gun_step,shootRate
def eachStepMove(step,shootRate):
    eachSleepTime=shootRate/step
    while step>0:
        start=time.perf_counter()
        pydirectinput.moveRel(0,1)
        step-=1
        end=time.perf_counter()
        duration=end-start
        wpt.sleep(eachSleepTime-duration)
def moveMouse():
    global is_left_button_pressed,gun
    gun_step,shootRate=getGunData()
    for step in gun_step:
        time_start=time.perf_counter()
        step=int(step)
        stepRemain=step
        eachNormalStep = step // globalConfig.stridesNum
        eachSleepTime=shootRate/globalConfig.stridesNum
        x_start, y_start = pyautogui.position()
        duration_sum=0
        if is_left_button_pressed:
            time_fire=time.perf_counter()
            timeList=[]
            exceptTimeList=[]
            for index in range(globalConfig.stridesNum):
                if stepRemain>=eachNormalStep:
                    fireStart = time.perf_counter()
                    pydirectinput.moveRel(None, eachNormalStep,relative=True,disable_mouse_acceleration=True)
                    stepRemain-=eachNormalStep
                    fireEnd = time.perf_counter()
                    # 记录每次移动鼠标所花费的时间，用于修正每阶段移动的睡眠时间
                    duration = fireEnd - fireStart
                    duration_sum = duration_sum + duration
                    # 使用重写的sleep函数，实现微秒级睡眠精度
                    wpt.sleep(eachSleepTime - duration)
                    # exceptTimeList.append((eachSleepTime - duration) * 1000)
                    # timeMoveEnd = time.perf_counter()
                    # timeList.append((timeMoveEnd - fireStart) * 1000)
                else:
                    pydirectinput.moveRel(None, stepRemain,relative=True,disable_mouse_acceleration=True)
                    stepRemain-=eachNormalStep
            x, y = pyautogui.position()
            print("结束位置", x, y,"移动步长：",y-y_start,"期望移动步长：",step)
            time_end = time.perf_counter()
            print("duration_sum",duration_sum*1000,"ms")
            print("移动时长：", (time_end - time_start)*1000, "ms", "期望移动时长", shootRate * 1000, "ms")
        else:
            break

def listenMouse():
    with mouse.Listener(on_click=on_click) as listener:
        listener.join()
def listenKeyboard():
    keyboardListener=keyboard.Listener(on_press=on_press,on_release=on_release)
    keyboardListener.start()
    # with keyboard.Listener(on_press=on_press,on_release=onrealease) as keyboardlistener:
    #     keyboardlistener.join()
def run():
    ThreadPool.pool.submit(listenKeyboard)
    ThreadPool.pool.submit(listenMouse)
    pydirectinput.PAUSE=0.0
    sys.exit(app.exec_())
    # while True:
    #     pass