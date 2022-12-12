"""Logger middleware module."""
# standard library
import logging
import os
import socket
from logging.handlers import RotatingFileHandler, SysLogHandler


class RotatingFileHandlerCustom(RotatingFileHandler):
    """Customized Rotating handler that will ensure log directory path is created."""

    def __init__(
        self,
        filename: str,
        mode: str | None = 'a',
        maxBytes: int | None = 0,
        backupCount: int | None = 0,
        encoding: str | None = None,
        delay: int | None = 0,
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
        level: int = logging.getLevelName(level.upper())
        if not isinstance(level, int):  # pragma: no cover
            # only valid levels will return a int. invalid numbers don't throw an exception.
            raise RuntimeError('Invalid logging level.')
    return level


def rotating_handler(
    backup_count: int | None = 10,
    directory: str | None = 'log',
    filename: str | None = 'server.log',
    formatter: logging.Formatter | None = None,
    level: str | None = 'INFO',
    max_bytes: int | None = 10_485_760,
    mode: str | None = 'a',
    name: str | None = 'rfh',
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
    host: str | None = 'localhost',
    facility: str | None = 'user',
    formatter: logging.Formatter | None = None,
    level: str | None = 'INFO',
    name: str | None = 'sh',
    port: int | None = 514,
    socktype: str | None = 'UDP',
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
