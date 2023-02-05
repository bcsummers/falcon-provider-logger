"""Falcon app used for testing."""
# third-party
import falcon

# first-party
from falcon_provider_logger.middleware import LoggerMiddleware
from falcon_provider_logger.utils import rotating_handler


class LoggerRotatingLoggerResource:
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
        resp.text = f'Logged - {key}'

    def on_post(self, req: falcon.Request, resp: falcon.Response) -> None:
        """Support POST method."""
        key: str = req.get_param('key')
        value: dict | int | list | str = req.get_param('value')
        self.log.debug(f'DEBUG {key} {value}')
        self.log.info(f'INFO {key} {value}')
        self.log.warning(f'WARNING {key} {value}')
        self.log.error(f'ERROR {key} {value}')
        self.log.critical(f'CRITICAL {key} {value}')
        resp.text = f'Logged - {key}'


rh: object = rotating_handler(level='debug')
app_rh_logger = falcon.App(middleware=[LoggerMiddleware([rh], name='SERVER-RFH')])
app_rh_logger.add_route('/middleware', LoggerRotatingLoggerResource())
