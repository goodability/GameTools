import logging as log
import sys
from config import globalConfig
from GUI import window,app

class Logging:
    def __init__(self):
        self.logging = log
        self.format = globalConfig.loggingFormat
        self.loggingLevel = globalConfig.loggingLevel
        self.setLogging()

    def setLogging(self):
        self.logging.basicConfig(level=self.loggingLevel, format=self.format)

    # def getLogging(self):
    #     return self.logging

    def info(self, message, **kwargs):
        self.logging.info(message)
        if "importantText" in kwargs.keys():
            window.showmessage(message,importantText=True)
        else:
            window.showmessage(message)

logging=Logging()
