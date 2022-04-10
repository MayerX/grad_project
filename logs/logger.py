# -*- coding: utf-8 -*-
import datetime
import logging


def logger():
    # 获得日期
    today = datetime.datetime.today()
    logger = logging.getLogger()
    # 设置日志级别
    logger.setLevel(logging.INFO)
    # 日志输出格式
    # formatter = logging.Formatter('%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
    formatter = logging.Formatter(fmt="%(levelname)s :%(asctime)s:%(filename)s[line:%(lineno)d] - %(message)s",
                                  datefmt="%Y-%m-%d %H:%M:%S")

    # 标准流处理器，设置的级别为WARAING
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    # 文件处理器，设置的级别为INFO
    file_handler = logging.FileHandler(filename='../logs/{}-{}-{}.log'.format(today.year, today.month, today.day),
                                       encoding='utf-8')
    file_handler.setLevel(level=0)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    logger.log(level=0, msg='\n -----Start Log-----')

    return logger


# 测试
if __name__ == '__main__':
    logger = logger()
    logger.info('info')
    logger.warning('warning')
    logger.debug('debug')
    logger.error('error')
