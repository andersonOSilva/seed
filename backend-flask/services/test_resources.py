import pytest
import requests

from models.user import UserModel


# test user
def test_post_user():
    response = requests.post(
        "http://localhost:5000/api/user",
        data={
            "id":666,
            "first_name": "teste",
            "last_name": "teste",
            "email": "jdfsklj@nxncx",
            "password": "sjdfjljslfdsj"
            })
    assert response.status_code == 201

def test_get_user():
    response = requests.get("http://localhost:5000/api/user")
    assert response.status_code == 200

def test_put_user():
    response = requests.put(
        "http://localhost:5000/api/user/1",
        data={
            "first_name": "testado",
            "email": "jdfsklj@nxncx"
            })
    assert response.status_code == 204


# test destroy
def test_destroy():
    try:
        user_response = requests.delete(f"http://localhost:5000/api/user/1")
    except Exception as e:
        print(e)
    assert user_response.status_code == 204
