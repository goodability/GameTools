import logging
import pydirectinput
'''
    系统全局配置参数
'''
loggingLevel=logging.DEBUG
loggingFormat="[%(asctime)s]---%(name)s---%(levelname)s---%(thread)d---%(message)s"
threadPoolMax=6
pydirectinput.PAUSE = 0.0
stridesNum=6

screenCatchXmin=0.6835
screenCatchYmin=0.0694
screenCatchYmax=0.5208

screenWidth=2560
screenHeight=1440

#用以定位判断是否打开背包
judgeBagBoxXmin=0.1953
judgeBagBoxYmin=0.0548
judgeBagBoxXmax=0.2238
judgeBagBoxYmax=0.0791

#用以定位是否打开了地图
judgeOpenMapXmin=0.8945
judgeOpenMapYmin=0.9083
judgeOpenMapXmax=0.9242
judgeOpenMapYmax=0.9208

#用以判断是否打开地图阈值
ifOpenMaptheadshold=80