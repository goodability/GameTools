import logging
import pydirectinput
'''
    系统全局配置参数
'''
loggingLevel=logging.INFO
loggingFormat="[%(asctime)s]---%(name)s---%(levelname)s---%(thread)d---%(message)s"
threadPoolMax=6
pydirectinput.PAUSE = 0.0
stridesNum=6

screenCatchXmin=0.6835
screenCatchYmin=0.0694
screenCatchYmax=0.5208

screenWidth=2560
screenHeight=1440

judgeBagBoxXmin=0.1953
judgeBagBoxYmin=0.0548
judgeBagBoxXmax=0.2238
judgeBagBoxYmax=0.0791
ifInBagtheadshold=70