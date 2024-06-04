from http import HTTPStatus

import pytest
from fastapi.testclient import TestClient

from fast_zero.app import app


@pytest.fixture()
def client():
    return TestClient(app)


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


def test_read_users(client):
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'users': [
            {
                'username': 'Joaquim',
                'email': 'joaquim@example.com',
                'id': 1,
            },
        ],
    }


def test_read_user(client):
    response = client.get('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'Joaquim',
        'email': 'joaquim@example.com',
        'id': 1,
    }


def test_read_user_exception(client):
    response = client.get('/users/2')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'user not found'}


def test_update_user(client):
    response = client.put(
        '/users/1',
        json={
            'username': 'Joaquim',
            'email': 'joaquim@example.com',
            'password': 'newsecret',
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'Joaquim',
        'email': 'joaquim@example.com',
        'id': 1,
    }


def test_update_user_exception(client):
    response = client.put(
        '/users/2',
        json={
            'username': 'Joaquim',
            'email': 'joaquim@example.com',
            'password': 'newsecret',
        },
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'user not found'}


def test_delete_user(client):
    response = client.delete('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'user deleted'}


def test_delete_user_exception(client):
    response = client.delete('/users/2')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'user not found'}
