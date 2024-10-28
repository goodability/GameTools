import logging
import pydirectinput
'''
    系统全局配置参数
'''
loggingLevel=logging.DEBUG
loggingFormat="[%(asctime)s]---%(name)s---%(levelname)s---%(thread)d---%(message)s"
threadPoolMax=15
pydirectinput.PAUSE = 0.0
stridesNum=5

screenCatchXmin=0.6835
screenCatchYmin=0.0694
screenCatchYmax=0.5208

screenWidth=2560
screenHeight=1440

#用以定位判断是否打开背包
judgeBagBoxXmin=0.1941
judgeBagBoxYmin=0.0541
judgeBagBoxXmax=0.2246
judgeBagBoxYmax=0.0805

#用以定位是否打开了地图
judgeOpenMapXmin=0.9007
judgeOpenMapYmin=0.9090
judgeOpenMapXmax=0.9574
judgeOpenMapYmax=0.9201

#用于判断是否开镜
judgeOpenMirrorXmin=0.4894
judgeOpenMirrorYmin=0.8173
judgeOpenMirrorXmax=0.5097
judgeOpenMirrorYmax=0.8256
#用以判断是否打开地图阈值
ifOpenMaptheadshold=80

#用于判断是否开镜的阈值
ifOpenMirror=70
#修正开枪间隔睡眠时间参数,3ms
sleepBiase=3

#游戏内垂直灵敏度
vertical=1.38