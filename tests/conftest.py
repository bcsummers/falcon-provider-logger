# -*- coding: utf-8 -*-
"""Testing conf module."""
# standard library
import os
import threading

# third-party
import pytest
from falcon import testing

from .Custom.app import app_custom_logger
from .Null.app import app_null_logger
from .Rotating_Logger.app import app_rh_logger
from .Syslog.syslog_server import TestSyslogServers

# the log directory for all test cases
_LOG_DIRECTORY = os.path.join(os.getcwd(), 'log')
test_syslog = TestSyslogServers(address='0.0.0.0', log_directory=_LOG_DIRECTORY)
tcp_server = test_syslog.start_tcp_server(port=5141)
udp_server = test_syslog.start_udp_server(port=5140)


@pytest.fixture
def client_custom() -> object:
    """Create testing client fixture for logger app"""
    return testing.TestClient(app_custom_logger)


@pytest.fixture
def client_null() -> object:
    """Create testing client fixture for logger app"""
    return testing.TestClient(app_null_logger)


@pytest.fixture
def client_rh() -> object:
    """Create testing client fixture for logger app"""
    return testing.TestClient(app_rh_logger)


@pytest.fixture
def client_sh_tcp() -> object:
    """Create testing client fixture for logger app"""
    # import here so tcp server can be started first in pytest_configure
    from .Syslog.app import app_sh_tcp_logger  # pylint: disable=import-outside-toplevel

    return testing.TestClient(app_sh_tcp_logger)


@pytest.fixture
def client_sh_udp() -> object:
    """Create testing client fixture for logger app"""
    # import here so udp server can be started first in pytest_configure
    from .Syslog.app import app_sh_udp_logger  # pylint: disable=import-outside-toplevel

    return testing.TestClient(app_sh_udp_logger)


@pytest.fixture
def log_directory() -> str:
    """Return the log directory."""
    return _LOG_DIRECTORY


def pytest_configure() -> None:
    """Clear the log directory after tests are complete"""
    # start TCP syslog servers
    tcp_thread = threading.Thread(name='tcp_server', target=tcp_server.serve_forever, daemon=True)
    tcp_thread.start()

    # start UDP syslog servers
    udp_thread = threading.Thread(name='udp_server', target=udp_server.serve_forever, daemon=True)
    udp_thread.start()


def pytest_unconfigure(config: object) -> None:  # pylint: disable=unused-argument
    """Clear the log directory after tests are complete"""
    if os.path.isdir(_LOG_DIRECTORY):
        for log_file in os.listdir(_LOG_DIRECTORY):
            file_path = os.path.join(_LOG_DIRECTORY, log_file)
            if os.path.isfile(file_path):
                os.unlink(file_path)
        os.rmdir(_LOG_DIRECTORY)
