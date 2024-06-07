from http import HTTPStatus


def test_get_token(client, user):
    response = client.post(
        'auth/token/',
        data={'username': user.email, 'password': user.clean_password},
    )
    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in token
    assert 'token_type' in token


def test_get_token_with_incorrect_username(client, user):
    response = client.post(
        'auth/token/',
        data={'username': 'tes@test.com', 'password': user.clean_password},
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_get_token_with_incorrect_password(client, user):
    response = client.post(
        'auth/token/',
        data={'username': user.email, 'password': 'secret'},
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
