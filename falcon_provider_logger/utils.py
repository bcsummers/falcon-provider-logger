# -*- coding: utf-8 -*-
"""Logger middleware module."""
# standard library
import logging
import os
import socket
from logging.handlers import RotatingFileHandler, SysLogHandler
from typing import Any, Optional


class RotatingFileHandlerCustom(RotatingFileHandler):
    """Customized Rotating handler that will ensure log directory path is created."""

    def __init__(
        self,
        filename: str,
        mode: Optional[str] = 'a',
        maxBytes: Optional[int] = 0,
        backupCount: Optional[int] = 0,
        encoding: Optional[str] = None,
        delay: Optional[int] = 0,
    ):
        """Create a customized RotatingFileHandler that supports creation of the full log path.

        Args:
            filename: The name of the logfile.
            mode: The write mode for the file.
            maxBytes: The max file size before rotating.
            backupCount: The maximum number of backup files.
            encoding: The log file encoding.
            delay: The delay period.
        """
        if not os.path.exists(os.path.dirname(filename)):
            os.makedirs(os.path.dirname(filename), exist_ok=True)
        RotatingFileHandler.__init__(self, filename, mode, maxBytes, backupCount, encoding, delay)


def get_level(level: str) -> int:
    """Return proper logging level.

    Args:
        level: The logging level.

    Raises:
        RuntimeError: Invalid level provide

    Returns:
        int: The logging level as an int.
    """
    if not isinstance(level, int):
        level: Any = logging.getLevelName(level.upper())
        if not isinstance(level, int):  # pragma: no cover
            # only valid levels will return a int. invalid numbers don't throw an exception.
            raise RuntimeError('Invalid logging level.')
    return level


def rotating_handler(
    backup_count: Optional[int] = 10,
    directory: Optional[str] = 'log',
    filename: Optional[str] = 'server.log',
    formatter: Optional[logging.Formatter] = None,
    # in 3.8 Literal[] could be used
    level: Optional[str] = 'INFO',
    max_bytes: Optional[int] = 10_485_760,
    # in 3.8 Literal[] could be used
    mode: Optional[str] = 'a',
    name: Optional[str] = 'rfh',
) -> RotatingFileHandlerCustom:
    """Return a configured instance of a rotating file handler with sane defaults.

    Args:
        backup_count: The number of backup log files to keep.
        directory: The directory to write the log file.
        filename: The name of the log file.
        formatter: A logging formatter to format logging handler.
            Defaults to a sane formatter with module/lineno.
        level: The logging level for the handler.
        name: The handler name.
        max_bytes: The maximum size of the log file.
        mode: The write mode for the log file.

    Returns:
        RotatingFileHandlerCustom: A customized instance of the RotatingFileHandler.
    """
    lh = RotatingFileHandlerCustom(
        os.path.join(directory, filename), backupCount=backup_count, maxBytes=max_bytes, mode=mode
    )
    lh.setLevel(get_level(level))
    if formatter is None:
        # a sane formatter that includes method and line number
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s '
            '[%(module)s:%(funcName)s:%(lineno)d]'
        )
    lh.setFormatter(formatter)
    lh.set_name(name)
    return lh


def syslog_handler(
    host: Optional[str] = 'localhost',
    facility: Optional[str] = 'user',
    formatter: Optional[logging.Formatter] = None,
    # in 3.8 Literal[] could be used
    level: Optional[str] = 'INFO',
    name: Optional[str] = 'sh',
    port: Optional[int] = 514,
    # in 3.8 Literal[] could be used
    socktype: Optional[str] = 'UDP',
) -> SysLogHandler:
    """Return a configured instance of a syslog handler with sane defaults.

    Args:
        host: The syslog hostname/ip.
        facility: The syslog facility.
        formatter: A logging formatter to format logging handler.
            Defaults to a sane formatter with module/lineno.
        level: The logging level for the handler.
        name: The handler name.
        port: The syslog port.
        socktype: The socket type. Either TCP or UDP.

    Returns:
        SyslogHandler: A configured instance of the SyslogHandler.
    """
    # build address from host and port
    address = (host, int(port))

    # set socktype
    if socktype.upper() == 'TCP':
        socktype = socket.SOCK_STREAM
    elif socktype.upper() == 'UDP':
        socktype = socket.SOCK_DGRAM  # default
    else:  # pragma: no cover
        raise RuntimeError(f'{socktype} is not a valid socktype.')

    # create the handler
    lh = SysLogHandler(address=address, facility=facility, socktype=socktype)
    lh.setLevel(get_level(level.upper()))
    if formatter is None:
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s '
            '[%(module)s:%(funcName)s:%(lineno)d]'
        )
    lh.setFormatter(formatter)
    lh.set_name(name)

    return lh
