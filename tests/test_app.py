from http import HTTPStatus

from fast_zero.schemas import UserPublic


def test_root_deve_retornar_ok_e_ola_mundo(client):
    response = client.get('/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Olá mundo!'}


def test_create_user(client):
    response = client.post(
        '/users/',
        json={
            'username': 'Joaquim',
            'email': 'joaquim@example.com',
            'password': 'secret',
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'username': 'Joaquim',
        'email': 'joaquim@example.com',
        'id': 1,
    }


def test_create_user_with_username_already_exists(client, user):
    response = client.post(
        '/users/',
        json={
            'username': 'test',
            'email': 'test@test.com',
            'password': 'secret',
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {
        'detail': 'username already exists',
    }


def test_create_user_with_email_already_exists(client, user):
    response = client.post(
        '/users/',
        json={
            'username': 'Joaquim',
            'email': 'test@test.com',
            'password': 'secret',
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {
        'detail': 'email already exists',
    }


def test_read_users(client):
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'users': [],
    }


def test_read_users_with_users(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/')

    assert response.json() == {'users': [user_schema]}


def test_read_user(client, user):
    response = client.get(f'/users/{user.id}')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'test',
        'email': 'test@test.com',
        'id': 1,
    }


def test_read_user_user_not_found(client):
    response = client.get('/users/2')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_update_user(client, user, token):
    response = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'bob',
            'email': 'bob@example.com',
            'password': 'newsecret',
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'bob',
        'email': 'bob@example.com',
        'id': user.id,
    }


def test_update_user_user_not_found(client, token):
    response = client.put(
        '/users/2',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'Joaquim',
            'email': 'joaquim@example.com',
            'password': 'newsecret',
        },
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_delete_user(client, user, token):
    response = client.delete(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


def test_delete_user_user_not_found(client, token):
    response = client.delete(
        '/users/2',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_get_token(client, user):
    response = client.post(
        '/token/',
        data={'username': user.email, 'password': user.clean_password},
    )
    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in token
    assert 'token_type' in token


def test_get_token_with_incorrect_username(client, user):
    response = client.post(
        '/token/',
        data={'username': 'tes@test.com', 'password': user.clean_password},
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_get_token_with_incorrect_password(client, user):
    response = client.post(
        '/token/',
        data={'username': user.email, 'password': 'secret'},
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
