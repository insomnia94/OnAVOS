#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: smasneri@vicomtech.org

"""A collection of functions used for logging, based on colorama"""

from colorama import Fore, Back, Style, AnsiToWin32
import logging
import sys


class ColorizingStreamHandler(logging.StreamHandler):
    color_map = {
        logging.DEBUG: Fore.CYAN,
        logging.WARNING: Style.BRIGHT + Fore.YELLOW,
        logging.ERROR: Style.BRIGHT + Fore.RED,
        logging.CRITICAL: Style.BRIGHT + Back.RED,
    }

    def __init__(self, stream, color_map=None):
        logging.StreamHandler.__init__(self, AnsiToWin32(stream).stream)
        if color_map is not None:
            self.color_map = color_map

    @property
    def is_tty(self):
        isatty = getattr(self.stream, 'isatty', None)
        return isatty and isatty()

    def format(self, record):
        message = logging.StreamHandler.format(self, record)
        if self.is_tty:
            # Don't colorize a traceback
            parts = message.split('\n', 1)
            parts[0] = self.colorize(parts[0], record)
            message = '\n'.join(parts)
        return message

    def colorize(self, message, record):
        try:
            return self.color_map[record.levelno] + message + Style.RESET_ALL
        except KeyError:
            return message


# Setup the logger
logger = logging.getLogger('test')
# Add colored logging functionalities
handler = ColorizingStreamHandler(sys.stdout)
formatter = logging.Formatter('[%(levelname)s]: %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

if __name__ == '__main__':
    handler = ColorizingStreamHandler(sys.stdout)
    formatter = logging.Formatter('%(levelname)s:%(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)

    logger.debug('debug message')
    logger.info('info message')
    logger.warning('warning message')
    logger.error('error message')
    logger.critical('critical message')
