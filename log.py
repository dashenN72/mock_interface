# -*- coding: utf-8 -*-
# @Time    : 2020/3/3 23:32
# @Author  : dashenN72

import logging
import time
"""
在工程中多个地方要实例化该TestLog类的时，注意使用不同的名字，及log=TestLog(logger='不同值')，否则hui'chu
"""


class TestLog(object):
    """
    封装后的logging
    """

    def __init__(self, logger=None):
        """
        指定保存日志的文件路径，日志级别，以及调用文件
        将日志存入到指定的文件中
        :param logger:
        """

        # 创建一个logger
        self.logger = logging.getLogger(logger)
        self.logger.setLevel(logging.DEBUG)
        # 创建一个handler，用于写入日志文件
        self.log_time = time.strftime("%Y_%m_%d_")
        self.log_path = ".\\log\\"
        self.log_name = self.log_path + self.log_time + '.log'

        # fh = logging.FileHandler(self.log_name, 'a')  # 追加模式  这个是python2的
        fh = logging.FileHandler(self.log_name, 'a', encoding='utf-8')  # 这个是python3的
        fh.setLevel(logging.INFO)

        # 再创建一个handler，用于输出到控制台
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)

        # 定义handler的输出格式,console和file不同的ri
        formatter_console = logging.Formatter('%(message)s')
        formatter_file = logging.Formatter(
            '[%(asctime)s] %(filename)s->%(funcName)s line:%(lineno)d [%(levelname)s]%(message)s')
        fh.setFormatter(formatter_file)
        ch.setFormatter(formatter_console)

        # 给logger添加handler
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)

        #  添加下面一句，在记录日志之后移除句柄
        # self.logger.removeHandler(ch)
        # self.logger.removeHandler(fh)
        # 关闭打开的文件
        fh.close()
        ch.close()

    def getlog(self):
        return self.logger


if __name__ == '__main__':
    log = TestLog().getlog()
    log.info("info message")
    log.debug("debug message")
    log.error("error message")
    log.critical("critical message")
