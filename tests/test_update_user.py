import pytest
import allure
from api_client import *

class TestUserUpdate:


    @allure.title('Изменение данных пользователя с авторизацией')
    @allure.description('Проверка что авторизованный пользователь может изменить свои данные. Ожидается статус 200 после каждого изменения')
    def test_update_user_with_auth(self):
        user, access_token = create_and_login_user()
        new_email = f"new_{user['email']}"
        new_name = f"new_{user['name']}"
        update_response = update_user_info(access_token, {
            "email": new_email,
            "name": new_name
        })
        assert update_response.status_code == 200
        response_data = update_response.json()
        assert response_data["user"]["email"] == new_email
        assert response_data["user"]["name"] == new_name
        delete_user(access_token)

    @allure.title('Ошибка изменения email без авторизации)')
    @allure.description('Попытка изменить данные пользователя без передачи токена авторизации. Ожидается ошибка 401')
    def test_update_user_without_auth_with_email(self):
        update_response = update_user_info("", {"email": "test@test.com"})
        assert update_response.status_code == 401
        assert "You should be authorised" in update_response.json()["message"]

    @allure.title('Ошибка изменения имени без авторизации')
    @allure.description('Попытка изменить данные пользователя без передачи токена авторизации. Ожидается ошибка 401')
    def test_update_user_without_auth_with_name(self):
        update_response = update_user_info("", {"name": "NewName"})
        assert update_response.status_code == 401
        assert "You should be authorised" in update_response.json()["message"]

        