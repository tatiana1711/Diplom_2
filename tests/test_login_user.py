import pytest
import allure
from api_client import *

class TestUserLogin:


    @allure.title('Успешный логин пользователя')
    @allure.description('Авторизация с правильными email и паролем. Ожидается статус 200 и наличие accessToken')
    def test_login_user_success(self):
        user_data = create_and_login_user()
        access_token = user_data[1]
        assert access_token is not None
        delete_user(access_token)


    @allure.title('Ошибка при логине с неверным паролем')
    @allure.description('Авторизация с правильным email но неверным паролем. Ожидается ошибка 401')
    def test_login_user_wrong_password_false(self):
        user, access_token = create_and_login_user() 
        login_payload = {"email": user["email"], "password": "wrong_password"}
        login_response = requests.post(f"{BASE_URL}/auth/login", json=login_payload)
        assert login_response.status_code == 401
        delete_user(access_token)


    @allure.title('Ошибка при логине с неверным email')
    @allure.description('Авторизация с неверным email но правильным паролем. Ожидается ошибка 401')
    def test_login_user_wrong_email_false(self):
        user, access_token = create_and_login_user()  
        login_payload = {"email": "wrong_email@test.com", "password": user["password"]}
        login_response = requests.post(f"{BASE_URL}/auth/login", json=login_payload)
        assert login_response.status_code == 401
        delete_user(access_token)


    @allure.title('Логин несуществующего пользователя')
    @allure.description('Авторизация с данными несуществующего пользователя. Ожидается ошибка 401')
    def test_login_nonexistent_user(self):
        fake_user = create_new_user()
        login_payload = {"email": fake_user["email"], "password": fake_user["password"]}
        login_response = requests.post(f"{BASE_URL}/auth/login", json=login_payload)
        assert login_response.status_code == 401

