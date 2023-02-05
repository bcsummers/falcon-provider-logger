"""Test logger middleware."""
# standard library
from uuid import uuid4

# third-party
from falcon.testing import Result


def test_default_get(client_null: object) -> None:
    """Test GET resource

    Args:
        client_null (fixture): The test client.
    """
    key = f'{uuid4()}'
    params = {'key': key}
    response: Result = client_null.simulate_get('/middleware', params=params)

    assert response.status_code == 200
    assert response.text == f'Logged - {key}'


def test_default_post(client_null: object) -> None:
    """Test POST resource

    Args:
        client_null (fixture): The test client.
    """
    key = f'{uuid4()}'
    params = {'key': key, 'value': 'middleware-worked'}
    response: Result = client_null.simulate_post('/middleware', params=params)

    assert response.status_code == 200
    assert response.text == f'Logged - {key}'
