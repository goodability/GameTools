from concurrent.futures import ThreadPoolExecutor
from config.log import Logging
from config import globalConfig
class ThreadPool:
    workers = globalConfig.threadPoolMax
    pool = ThreadPoolExecutor(max_workers=workers)
    def __init__(self):
        self.logging=Logging().getLogging()
        self.logging.info("线程池最大线程数为:"+str(self.workers))
    def submit(self,function):
        self.pool.submit(function)
        self.logging.info("线程已被提交到线程池！")