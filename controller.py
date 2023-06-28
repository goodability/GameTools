import random
import threading
import time
import cv2
from person import posture
from pynput.keyboard import Key
from config.log import Logging
from config import gunConfig,globalConfig
from pynput import keyboard,mouse
from pynput.mouse import Controller
from threadPool import ThreadPool
import pydirectinput
from fittingDetect.imgDeal import imageCoper
STATUS=-1
fittingWeights=1
isSquat=False
isGrovel=False
holdKeyFlag=False
isHoldBreath=False
is_left_button_pressed=False
gun=None
logging=Logging().getLogging()
is_open_mirror=False#按下鼠标右键代表按下右键
imgcoper=imageCoper()
def on_press(key):
    global STATUS,gun,isSquat,isGrovel,isHoldBreath,fittingWeights,is_open_mirror
    try:
        if key==Key.caps_lock:
            STATUS=STATUS*-1
            if STATUS==1:
                logging.info("开关打开！")
            else:
                logging.info("开关关闭！")
        #开关打开才能选择枪械
        if STATUS==1:
            # print(key),type(key)
            if key==Key.end or str(key)=='<97>':
                logging.info("选择枪械m762！")
                gun="m762"
            elif key==Key.down or str(key)=='<98>':
                logging.info("选择枪械ace！")
                gun="ace"
            #识别配件
            elif key==Key.tab:
                fittingWeights=imgcoper.classfyAllFitting()
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
            elif key==Key.space:
                isGrovel=False
                isSquat=False
            #屏息
            elif key==Key.shift and isHoldBreath==False:
                isHoldBreath=True
            #重置人物姿态，站立，不屏息
            elif key==Key.enter:
                [isGrovel,isHoldBreath,isSquat,is_open_mirror]=posture.resetPosture(isGrovel,isHoldBreath,isSquat,is_open_mirror)
                logging.info("重置人物姿态")
    except:
        logging.error("未知错误...")
def on_release(key):
    global isHoldBreath
    if key==Key.shift:
        isHoldBreath=False
def on_click(x,y,button,pressed):
    if STATUS==1:
        global is_left_button_pressed,is_open_mirror
        if button == mouse.Button.left:
            is_left_button_pressed = pressed
            if pressed and is_open_mirror:
                ThreadPool.pool.submit(moveMouse)
        elif button==mouse.Button.right:
            BagImg=imgcoper.getBagImg()
            ifInbag=imgcoper.classIsInBag(BagImg)
            if not ifInbag:
                if is_open_mirror:
                    is_open_mirror=False
                else:
                    is_open_mirror=True

def getGunData():
    global gun,isSquat,isGrovel,isHoldBreath,fittingWeights
    if gun=="m762":
        gun_step=gunConfig.m762_step
        shootRate=gunConfig.m762_fire_rate
    elif gun=="ace":
        gun_step=gunConfig.ace_step
        shootRate=gunConfig.ace_fire_rate
    else:
        logging.error("非法按键，没有对应的装备")
        raise RuntimeError("运行过程错误")
    stepWeight=posture.getPostureWeight(isGrovel,isHoldBreath,isSquat)
    logging.info("开枪姿态后座控制权重"+str(stepWeight)+"---配件后座控制权重"+str(fittingWeights))
    gun_step=gun_step*stepWeight*fittingWeights
    return gun_step,shootRate
def moveMouse():
    global is_left_button_pressed,gun
    gun_step,shootRate=getGunData()
    for step in gun_step:
        step=int(step)
        stepRemain=step
        if is_left_button_pressed:
            for each in range(globalConfig.stridesNum):
            #     mouseController.move(0,step//6)1
            #
            #     time.sleep(0.011)
                if stepRemain>=globalConfig.stridesNum:
                    pydirectinput.moveRel(0, step//globalConfig.stridesNum,relative=True)
                    stepRemain-=step//globalConfig.stridesNum
                else:
                    pydirectinput.moveRel(0, stepRemain, relative=True)
                time.sleep(shootRate/globalConfig.stridesNum)
            # time.sleep(shootRate+10)

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
    listenKeyboard()
    listenMouse()
    while True:
        pass