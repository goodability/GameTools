from threadPool import ThreadPool
from config.log import logging
from pynput import mouse, keyboard
from GUI import app
import sys
import controller


def Start():
    logging.info("开始侦听设备...")
    controller.run()


if __name__ == '__main__':

    Start()
