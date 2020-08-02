# -*- coding: utf-8 -*-
"""Test logger middleware."""
# standard library
from uuid import uuid4

# third-party
from falcon.testing.client import Result


def test_custom_get(client_custom: object) -> None:
    """Testing GET resource

    Args:
        client_custom (fixture): The test client.
    """
    key = f'{uuid4()}'
    params = {'key': key}
    response: Result = client_custom.simulate_get('/middleware', params=params)
    assert response.status_code == 200
    assert response.text == f'Logged - {key}'
