"""
Copyright (c) 2020 RoZetta Technology Pty Ltd. All rights reserved.
"""
import logging


def get_logger(name=None):
    logger = logging.getLogger(name)
    return logger
