# -*- coding: utf-8 -*-
#
# Tencent is pleased to support the open source community by making QTA available.
# Copyright (C) 2016THL A29 Limited, a Tencent company. All rights reserved.
# Licensed under the BSD 3-Clause License (the "License"); you may not use this
# file except in compliance with the License. You may obtain a copy of the License at
#
# https://opensource.org/licenses/BSD-3-Clause
#
# Unless required by applicable law or agreed to in writing, software distributed
# under the License is distributed on an "AS IS" basis, WITHOUT WARRANTIES OR CONDITIONS
# OF ANY KIND, either express or implied. See the License for the specific language
# governing permissions and limitations under the License.
#
"""log模块
"""

import logging
import sys
import traceback
import inspect
from testbase import context
from testbase.util import ensure_binary_stream, smart_binary

_stream, _encoding = ensure_binary_stream(sys.stdout)

class _Formatter(logging.Formatter):
    def format(self, record):
        s = super(_Formatter, self).format(record)
        return smart_binary(s, encoding=_encoding)


_stream_handler = logging.StreamHandler(_stream)
_stream_handler.terminator = b"\n"
_stream_handler.setFormatter(_Formatter())


class TestResultBridge(logging.Handler):
    """中转log信息到TestResult"""

    def emit(self, log_record):
        """Log Handle 必须实现此函数"""
        testresult = context.current_testresult()
        formatted_msg = self.format(log_record)
        if testresult is None:
            _stream_handler.emit(log_record)
            return
        record = {}
        if log_record.exc_info:
            record["traceback"] = "".join(
                traceback.format_tb(log_record.exc_info[2])
            ) + "%s: %s" % (log_record.exc_info[0].__name__, log_record.exc_info[1])
        testresult.log_record(log_record.levelno, formatted_msg, record)


_LOGGER_NAME = "QTA_LOGGER"
_logger = logging.getLogger(_LOGGER_NAME)
_logger.setLevel(logging.DEBUG)
_testresult_bridge = TestResultBridge()
_logger.addHandler(_testresult_bridge)


def critical(msg, *args, **kwargs):
    _logger.error(msg, *args, **kwargs)


fatal = critical


def error(msg, *args, **kwargs):
    """Log a message with severity 'ERROR' on the root logger."""
    _logger.error(msg, *args, **kwargs)


def exception(msg, *args):
    """Log a message with severity 'ERROR' on the root logger,with exception information."""
    _logger.exception(msg, *args)


def warning(msg, *args, **kwargs):
    """Log a message with severity 'WARNING' on the root logger."""
    _logger.warning(msg, *args, **kwargs)


warn = warning


def info(msg, *args, **kwargs):
    """Log a message with severity 'INFO' on the root logger."""
    _logger.info(msg, *args, **kwargs)


def debug(msg, *args, **kwargs):
    """Log a message with severity 'DEBUG' on the root logger."""
    _logger.debug(msg, *args, **kwargs)


def log(level, msg, *args, **kwargs):
    """Log 'msg % args' with the integer severity 'level' on the root logger."""
    _logger.log(level, msg, *args, **kwargs)


def addHandler(hdlr):  # pylint: disable=invalid-name
    """Add the specified handler to this logger."""
    _logger.addHandler(hdlr)


def removeHandler(hdlr):  # pylint: disable=invalid-name
    """Remove the specified handler from this logger."""
    _logger.removeHandler(hdlr)

def set_formatter(fmt):
    """Set the specified formatter to this logger.
    """
    class __Formatter(_Formatter):
        def __init__(self, fmt):
            super(_Formatter, self).__init__(fmt)

    class _CustomFormatter(logging.Formatter):
        def format(self, record):
            # Get the code line number and file name of the call logger function.
            logger_module = "logger"
            for frame_info in inspect.stack():
                frame = frame_info[0]
                module_name = inspect.getmodulename(frame.f_code.co_filename)
                if module_name != "__init__" and module_name != logger_module:
                    caller = inspect.getframeinfo(frame)
                    break
            else:
                return super(_CustomFormatter, self).format(record)
            record.filename = caller.filename.split('/')[-1]
            record.lineno = caller.lineno
            return super(_CustomFormatter, self).format(record)

    _stream_handler.setFormatter(__Formatter(fmt))
    _testresult_bridge.setFormatter(_CustomFormatter(fmt))

def set_level(level):
    """Set the specified log level to this logger.
    """
    _logger.setLevel(level)
