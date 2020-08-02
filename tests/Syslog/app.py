# -*- coding: utf-8 -*-
"""Falcon app used for testing."""
# standard library
from typing import Any

# third-party
import falcon

# first-party
from falcon_provider_logger.middleware import LoggerMiddleware
from falcon_provider_logger.utils import syslog_handler


class LoggerSyslogTcpResource:
    """Logger middleware testing resource."""

    log = None

    def on_get(self, req: falcon.Request, resp: falcon.Response) -> None:
        """Support GET method."""
        key: str = req.get_param('key')
        self.log.debug(f'DEBUG {key}')
        self.log.info(f'INFO {key}')
        self.log.warning(f'WARNING {key}')
        self.log.error(f'ERROR {key}')
        self.log.critical(f'CRITICAL {key}')
        resp.body = f'Logged - {key}'

    def on_post(self, req: falcon.Request, resp: falcon.Response) -> None:
        """Support POST method."""
        key: str = req.get_param('key')
        value: Any = req.get_param('value')
        self.log.debug(f'DEBUG {key} {value}')
        self.log.info(f'INFO {key} {value}')
        self.log.warning(f'WARNING {key} {value}')
        self.log.error(f'ERROR {key} {value}')
        self.log.critical(f'CRITICAL {key} {value}')
        resp.body = f'Logged - {key}'


sh: object = syslog_handler(level='debug', host='0.0.0.0', name='tcp', port=5141, socktype='TCP')
app_sh_tcp_logger = falcon.API(middleware=[LoggerMiddleware([sh], name='SERVER-TCP')])
app_sh_tcp_logger.add_route('/middleware', LoggerSyslogTcpResource())


class LoggerSyslogUdpResource:
    """Logger middleware testing resource."""

    log = None

    def on_get(self, req: falcon.Request, resp: falcon.Response) -> None:
        """Support GET method."""
        key: str = req.get_param('key')
        self.log.debug(f'DEBUG {key}')
        self.log.info(f'INFO {key}')
        self.log.warning(f'WARNING {key}')
        self.log.error(f'ERROR {key}')
        self.log.critical(f'CRITICAL {key}')
        resp.body = f'Logged - {key}'

    def on_post(self, req: falcon.Request, resp: falcon.Response) -> None:
        """Support POST method."""
        key: str = req.get_param('key')
        self.log.debug(f'DEBUG {key}')
        self.log.info(f'INFO {key}')
        self.log.warning(f'WARNING {key}')
        self.log.error(f'ERROR {key}')
        self.log.critical(f'CRITICAL {key}')
        resp.body = f'Logged - {key}'


sh: object = syslog_handler(level='debug', host='0.0.0.0', name='udp', port=5140)
app_sh_udp_logger = falcon.API(middleware=[LoggerMiddleware([sh], name='SERVER-UDP')])
app_sh_udp_logger.add_route('/middleware', LoggerSyslogUdpResource())
