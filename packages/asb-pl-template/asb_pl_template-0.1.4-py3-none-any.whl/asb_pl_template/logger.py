#!/usr/bin/env python
# -*- coding:utf8 -*-
import logging


def setup_logger(name, level=logging.INFO):
    """设置日志记录器"""
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # 检查是否已经有 StreamHandler
    has_stream_handler = False
    for handler in logger.handlers:
        if isinstance(handler, logging.StreamHandler):
            has_stream_handler = True
            break

    if not has_stream_handler:
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

    return logger


logger = setup_logger('asb-pl-template')
