"""Test logger middleware."""
# standard library
import os
import time
from uuid import uuid4

# third-party
from falcon.testing import Result


def has_text(logfile: str, text: str) -> bool:
    """Search for unique text in log file.

    Args:
        logfile: The fully qualified path to the logfile.
        text: The text to search for in the logfile.

    Returns:
        bool: True if text is found, else False.
    """
    time.sleep(0.10)  # allow time for log to flush
    with open(logfile, encoding='utf-8') as fh:
        for line in fh.read().strip().split('\n'):
            if text in line:
                break
        else:
            return False
    return True


def test_tcp_syslog_get(client_sh_tcp: object, log_directory: str) -> None:
    """Testing GET resource

    Args:
        client_sh_tcp (fixture): The test client.
        log_directory (fixture): The fully qualified path for the log directory.
    """
    logfile: str = os.path.join(log_directory, 'syslog_server.log')
    key = f'{uuid4()}'
    params = {'key': key}
    response: Result = client_sh_tcp.simulate_get('/middleware', params=params)

    assert response.status_code == 200
    assert response.text == f'Logged - {key}'
    for level in ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']:
        text = f'SERVER-TCP - {level} - {level} {key}'
        assert has_text(logfile, text) is True, f'Failed to find text {text}'


def test_tcp_syslog_post(client_sh_tcp: object, log_directory: str) -> None:
    """Testing POST resource

    Args:
        client_sh_tcp (fixture): The test client.
        log_directory (fixture): The fully qualified path for the log directory.
    """
    logfile: str = os.path.join(log_directory, 'syslog_server.log')
    key = f'{uuid4()}'
    params = {'key': key}
    response: Result = client_sh_tcp.simulate_post('/middleware', params=params)

    assert response.status_code == 200
    assert response.text == f'Logged - {key}'
    for level in ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']:
        text = f'SERVER-TCP - {level} - {level} {key}'
        assert has_text(logfile, text) is True, f'Failed to find text {text}'


def test_udp_syslog_get(client_sh_udp: object, log_directory: str) -> None:
    """Testing GET resource

    Args:
        client_sh_udp (fixture): The test client.
        log_directory (fixture): The fully qualified path for the log directory.
    """
    logfile: str = os.path.join(log_directory, 'syslog_server.log')
    key = f'{uuid4()}'
    params = {'key': key}
    response: Result = client_sh_udp.simulate_get('/middleware', params=params)

    assert response.status_code == 200
    assert response.text == f'Logged - {key}'
    for level in ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']:
        text = f'SERVER-UDP - {level} - {level} {key}'
        assert has_text(logfile, text) is True, f'Failed to find text {text}'


def test_udp_syslog_post(client_sh_udp: object, log_directory: str) -> None:
    """Testing GET resource

    Args:
        client_sh_udp (fixture): The test client.
        log_directory (fixture): The fully qualified path for the log directory.
    """
    logfile: str = os.path.join(log_directory, 'syslog_server.log')
    key = f'{uuid4()}'
    params = {'key': key}
    response: Result = client_sh_udp.simulate_post('/middleware', params=params)

    assert response.status_code == 200
    assert response.text == f'Logged - {key}'
    for level in ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']:
        text = f'SERVER-UDP - {level} - {level} {key}'
        assert has_text(logfile, text) is True, f'Failed to find text {text}'
