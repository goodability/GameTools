from threadPool import ThreadPool
from config.log import  Logging
from pynput import mouse,keyboard
import controller
def Start():
    logging=Logging().getLogging()
    logging.info("开始侦听设备...")
    controller.run()
if __name__ == '__main__':
    Start()