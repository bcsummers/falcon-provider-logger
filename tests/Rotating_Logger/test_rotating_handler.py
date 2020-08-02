# -*- coding: utf-8 -*-
"""Test logger middleware."""
# standard library
import os
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
    with open(logfile, 'r') as fh:
        for line in fh.read().strip().split('\n'):
            if text in line:
                break
        else:
            return False
    return True


def test_default_get(client_rh: object, log_directory: str) -> None:
    """Testing GET resource

    Args:
        client_rh (fixture): The test client.
        log_directory (fixture): The fully qualified path for the log directory.
    """
    logfile: str = os.path.join(log_directory, 'server.log')
    key = f'{uuid4()}'
    params = {'key': key}
    response: Result = client_rh.simulate_get('/middleware', params=params)

    assert response.status_code == 200
    assert response.text == f'Logged - {key}'
    # validate log file
    assert os.path.isfile(logfile)
    assert os.stat(logfile).st_size != 0
    for level in ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']:
        text = f'SERVER-RFH - {level} - {level} {key}'
        assert has_text(logfile, text) is True, f'Failed to find text {text}'


def test_default_post(client_rh, log_directory):
    """Testing GET resource

    Args:
        client_rh (fixture): The test client.
        log_directory (fixture): The fully qualified path for the log directory.
    """
    logfile: str = os.path.join(log_directory, 'server.log')
    key = f'{uuid4()}'
    params = {'key': key, 'value': 'middleware-worked'}
    response: Result = client_rh.simulate_post('/middleware', params=params)

    assert response.status_code == 200
    assert response.text == f'Logged - {key}'
    # validate log file
    assert os.path.isfile(logfile)
    assert os.stat(logfile).st_size != 0
    for level in ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']:
        text = f'SERVER-RFH - {level} - {level} {key}'
        assert has_text(logfile, text) is True, f'Failed to find text {text}'
