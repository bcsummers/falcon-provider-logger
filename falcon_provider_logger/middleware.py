"""Falcon logger middleware module."""
# standard library
import logging


class LoggerMiddleware:
    """Logger middleware provider."""

    def __init__(
        self,
        handlers: list[object] | None = None,
        level: str | None = 'DEBUG',
        name: str | None = 'SERVER',
        logger: logging.Logger | None = None,
    ):
        """Initialize class properties.

        Args:
            handlers: list of logging handlers to add to logger.
            level: The logger level.
            name: The logger name as displayed in the log file.
            logger: A pre-configured logger instance.
        """
        handlers: list = handlers or []

        if logger is not None:
            if not isinstance(logger, logging.Logger):  # pragma: no cover
                # ensure a proper input for logger is provided
                raise RuntimeError('Invalid input for logger.')
            self.log: object = logger
        else:
            self.log: object = logging.getLogger(name)
            self.log.setLevel(self.get_level(level))

        for h in handlers:
            # add logging handlers
            self.log.addHandler(h)

    @staticmethod
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
            level = logging.getLevelName(level.upper())
            if not isinstance(level, int):  # pragma: no cover
                # only valid levels will return a int. invalid numbers don't throw an exception.
                raise RuntimeError('Invalid logging level.')
        return level

    def process_resource(self, req, resp, resource, params):  # pylint: disable=unused-argument
        """Process resource method."""
        resource.log = self.log
