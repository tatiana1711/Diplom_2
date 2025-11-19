import pytest
import allure
import requests
from api_client import *

class TestCreateUser:


    @allure.title('Успешное создание уникального пользователя')
    @allure.description('Создание нового пользователя с валидными данными. Ожидается статус 200 и success: true')
    def test_success_create_user(self):
        payload = create_new_user()
        response = requests.post(f"{BASE_URL}/auth/register", json=payload)
        assert response.status_code == 200
        assert response.json().get("success") is True
        access_token = response.json().get("accessToken")
        if access_token:
            delete_user(access_token)

    @allure.title('Создание пользователя, который уже зарегистрирован')
    @allure.description('Попытка создать пользователя с уже существующими данными. Ожидается ошибка 403 и сообщение о дубликате')
    def test_create_existing_user(self):
        payload = create_new_user()
        first_response = requests.post(f"{BASE_URL}/auth/register", json=payload)
        assert first_response.status_code == 200
        second_response = requests.post(f"{BASE_URL}/auth/register", json=payload)
        assert second_response.status_code == 403
        assert second_response.json()["success"] is False
        assert second_response.json()["message"] == "User already exists"
        access_token = first_response.json().get("accessToken")
        if access_token:
            delete_user(access_token)

    @allure.title('Нельзя создать пользователя без email')
    @allure.description('Попытка создать пользователя не передавая в сообщении email. Ожидается ошибка 403 и сообщение о незаполненных обязательных полях')
    def test_create_user_without_email_false(self):
        payload = create_new_user() 
        payload.pop("email")
        response = requests.post(f"{BASE_URL}/auth/register", json=payload)
        assert response.status_code == 403
        assert "Email, password and name are required fields" in response.json()["message"]
        assert response.json()["success"] is False

    @allure.title('Нельзя создать пользователя без пароля')
    @allure.description('Попытка создать пользователя не передавая в сообщении пароль. Ожидается ошибка 403 и сообщение о незаполненных обязательных полях')
    def test_create_user_without_password_false(self):
        payload = create_new_user() 
        payload.pop("password")
        response = requests.post(f"{BASE_URL}/auth/register", json=payload)
        assert response.status_code == 403
        assert "Email, password and name are required fields" in response.json()["message"]
        assert response.json()["success"] is False

    @allure.title('Нельзя создать пользователя без имени')
    @allure.description('Попытка создать пользователя не передавая в сообщении имя пользователя. Ожидается ошибка 403 и сообщение о незаполненных обязательных полях')
    def test_create_user_without_name_false(self):
        payload = create_new_user() 
        payload.pop("name")
        response = requests.post(f"{BASE_URL}/auth/register", json=payload)
        assert response.status_code == 403
        assert "Email, password and name are required fields" in response.json()["message"]
        assert response.json()["success"] is False
