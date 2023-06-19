import logging
from config import globalConfig
class Logging:
    def __init__(self):
        self.logging=logging
        self.format=globalConfig.loggingFormat
        self.loggingLevel=globalConfig.loggingLevel
        self.setLogging()
    def setLogging(self):
        self.logging.basicConfig(level=self.loggingLevel,format=self.format)
    def getLogging(self):
        return self.logging
