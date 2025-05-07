"""
This module handles logging setup for Loguru.
Simply call setup_logging() for one-time setup and use Loguru for logging:
    from loguru import logger
    from logging_setup import setup_logging
    setup_logging(level='trace')
    logger.info("I am informational!")

LOG_FMT_HELP and LOG_LVL_HELP are avaliable for use in command-line help messages.
"""

import json
import logging as stdlib_logging
import sys
import warnings
from inspect import currentframe

import loguru
from loguru import _colorama as loguru_colorama
from loguru import logger as loguru_logger

from .dynamic_object_proxy import DynamicObjectProxy


# command-line help messages
LOG_FMT_HELP = "Logging format: auto, pretty, json"
LOG_LVL_HELP = "Logging level: trace, debug, info, success, warning, critical"

# add here noisy pieces of crap
disabled_loggers = [
]

logging_initialized = False
original_showwarning = warnings.showwarning


class InterceptHandler(stdlib_logging.Handler):
    def emit(self, record: stdlib_logging.LogRecord) -> None:
        # get corresponding loguru level if it exists.
        level: str | int
        try:
            level = loguru_logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # find caller from where originated the logged message
        frame, depth = currentframe(), 0
        while frame and (depth == 0 or frame.f_code.co_filename == stdlib_logging.__file__):
            frame = frame.f_back
            depth += 1

        loguru_logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


def loguru_showwarning(message, *args, **kwargs):
    # @todo this shows this file as the source of the log message, it should show the warning location instead
    loguru_logger.warning(message)
    original_showwarning(message, *args, **kwargs)


def json_formatter(record):
    to_serialize = {
        'timestamp': record['time'].isoformat(),
        'level': record['level'].name,
        'message': record['message'],
        'context': record['extra'],
        'exception': record['exception'].value if record['exception'] else None,
        'location': {
            'logger': record['name'],
            'module': record['module'],
            'function': record['function'],
            'line': record['line'],
            # 'file': record['file'].path,
            # "process": {"id": record["process"].id, "name": record["process"].name},
            # "thread": {"id": record["thread"].id, "name": record["thread"].name},
        },
    }
    serialized = json.dumps(to_serialize, default=repr)
    record['serialized'] = serialized
    return "{serialized}\n"


def interactive_formatter(record):
    ctx_vars_fmt = ""
    for k in record['extra']:
        # if a key in extra has an escape sequence this wont work
        ctx_vars_fmt += f"<magenta>{k}</magenta>=<cyan>{{extra[{k}]!s}}</cyan> "

    # this is nice but would break with file redirection. proper implementation would need a patch to loguru
    # OSC 8 format for terminal links
    # TERMINAL_LINK_FMT = "\033]8;;{link}\033\\{label}\033]8;;\033\\"
    # file_link = TERMINAL_LINK_FMT.format(
    #     link="file://{file.path}",
    #     label="{file.name}:{line}",
    # )

    ret = "<green>{time:HH:mm:ss}</green> <dim>|</dim> "
    ret += "<level>{level: <8}</level> <dim>|</dim> "
    ret += "{message} "
    ret += ctx_vars_fmt + "<dim>|</dim> "
    ret += "<dim>{name}:{function}:{line}</dim>"
    ret += "\n"
    ret += "{exception}"
    return ret


def setup_logging(log_format='auto', level='debug'):
    """
    Setup Loguru and redirect stdlib logging messages to it.
    log_format: 'auto', 'json', 'pretty'
    level: 'trace', 'debug', 'info', 'success', 'warning', 'critical', or integer level
    """

    global logging_initialized
    if logging_initialized:
        raise Exception("Tried to setup logging twice!")

    # DynamicObjectProxy enables loguru to pick up runtime changes to sys.stderr, in particular rich console redirections
    stream = DynamicObjectProxy(lambda: sys.stderr)
    if isinstance(level, str):
        level = level.upper()

    # hijack loguru logic decide between json and pretty logging
    if log_format == 'auto':
        if loguru_colorama.should_colorize(stream):
            log_format = 'pretty'
        else:
            log_format = 'json'

    stdlib_logging.basicConfig(
        handlers=[InterceptHandler()],
        level=stdlib_logging.NOTSET,
        force=True,
    )
    warnings.showwarning = loguru_showwarning
    for to_disable in disabled_loggers:
        loguru_logger.disable(to_disable)

    loguru_logger.remove()
    if log_format == 'pretty':
        loguru_logger.add(stream, format=interactive_formatter, level=level, diagnose=True)
    elif log_format == 'json':
        loguru_logger.add(stream, format=json_formatter, level=level)
    else:
        raise ValueError(f"Invalid {log_format=}")
    logging_initialized = True
