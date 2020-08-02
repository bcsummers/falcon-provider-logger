# -*- coding: utf-8 -*-
"""Falcon app used for testing."""
# standard library
import logging
from typing import Any

# third-party
import falcon

# first-party
from falcon_provider_logger.middleware import LoggerMiddleware


class LoggerCustomLoggerResource:
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


logger: object = logging.getLogger('custom')
app_custom_logger = falcon.API(middleware=[LoggerMiddleware(logger=logger)])
app_custom_logger.add_route('/middleware', LoggerCustomLoggerResource())
