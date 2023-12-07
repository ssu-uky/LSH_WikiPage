import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from .models import User

client = APIClient()


@pytest.fixture()
def create_user(django_user_model):
    user = django_user_model.objects.create(
        username="testuser",
        name="testname",
    )
    user.set_password("test123")
    user.save()
    return user


@pytest.mark.django_db
def test_create_user(create_user):
    """
    유저 생성 테스트
    """
    url = reverse("signup")
    data = {
        "username": "newtestuser",
        "name": "newtestname",
        "password": "newtest123",
    }
    response = client.post(url, data, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    assert User.objects.count() == 2
    assert User.objects.get(username="newtestuser").name == "newtestname"
    assert response.data["message"] == "newtestuser님, 회원가입이 완료되었습니다."


@pytest.mark.django_db
def test_fail_create_user(create_user):
    """
    유저 생성 실패 테스트
    """
    url = reverse("signup")
    data = {
        "username": "newtestuser",
        "name": "newtestname",
    }
    response = client.post(url, data, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert User.objects.count() == 1
    assert response.data["password"][0] == "이 필드는 필수 항목입니다."


@pytest.mark.django_db
def test_login(create_user):
    """
    로그인 테스트
    """
    url = reverse("login")
    data = {
        "username": "testuser",
        "password": "test123",
    }
    response = client.post(url, data, format="json")
    assert response.status_code == status.HTTP_200_OK
    assert response.data["message"] == "testuser님, 로그인 되었습니다."


@pytest.mark.django_db
def test_fail_login(create_user):
    """
    로그인 실패 테스트
    """
    url = reverse("login")
    data = {
        "username": "testuser",
        "password": "test1234",
    }
    response = client.post(url, data, format="json")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.data["message"] == "아이디 또는 비밀번호가 일치하지 않습니다."


@pytest.mark.django_db
def test_logout(create_user):
    """
    로그아웃 테스트
    """
    url = reverse("logout")
    client.login(username="testuser", password="test123")
    response = client.post(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["message"] == "로그아웃 되었습니다."
