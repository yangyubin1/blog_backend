# -*- coding: utf-8 -*-
__author__ = 'yubin.yang'
__date__ = '2018/5/2 16:39'

import logging
from logging import handlers

# 文件为：send_mail.log
# LOG_FILE = "/app/yunwei/p2p/ppc_monitor/run.log"
LOG_FILE = "log/run.log"
handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes=1024 * 1024, backupCount=5)  # 实例化handler
# 规范时间格式
fmt = '%(asctime)s - %(filename)s:%(lineno)s - %(name)s - %(message)s'
formatter = logging.Formatter(fmt)  # 实例化formatter
handler.setFormatter(formatter)  # 为handler添加formatter
logger = logging.getLogger(LOG_FILE)  # 获取名为prod_uss_bip.log的logger
logger.addHandler(handler)  # 为logger添加handler
logger.setLevel(logging.INFO)
