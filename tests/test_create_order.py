import pytest
import allure
from api_client import *

class TestCreateOrder:

    @allure.title('Создание заказа с авторизацией и ингредиентами')
    @allure.description('Создание заказа авторизованным пользователем с валидными ингредиентами. Ожидается статус 200 и success: true')
    def test_create_order_with_auth_and_ingredients(self):
        user_data = create_and_login_user()
        access_token = user_data[1]
        ingredients = get_valid_ingredient_ids(2)
        response = create_order(access_token, ingredients)
        assert response.status_code == 200
        assert response.json()["success"] is True
        delete_user(access_token)


    @allure.title('Создание заказа без авторизации с ингредиентами')
    @allure.description('Создание заказа без авторизации но с валидными ингредиентами. Ожидается статус 200 (неавторизованные пользователи могут создавать заказы)')
    def test_create_order_without_auth_with_ingredients(self):
        ingredients = get_valid_ingredient_ids(2)
        response = create_order(None, ingredients)
        assert response.status_code == 200
        assert response.json()["success"] is True


    @allure.title('Ошибка создания заказа без ингредиентов')
    @allure.description('Попытка создать заказ без передачи ингредиентов. Ожидается ошибка 400 с соответствующим сообщением')
    def test_create_order_without_ingredients(self):
        user_data = create_and_login_user()
        access_token = user_data[1]
        response = create_order(access_token, [])
        assert response.status_code == 400
        assert response.json()["success"] is False
        assert "Ingredient ids must be provided" in response.json()["message"]
        delete_user(access_token)


    @allure.title('Ошибка создания заказа с неверным хешем ингредиентов')
    @allure.description('Попытка создать заказ с невалидными ID ингредиентов. Ожидается ошибка 500 Internal Server Error')
    def test_create_order_with_invalid_ingredient_hash(self):
        user_data = create_and_login_user()
        access_token = user_data[1]
        response = create_order(access_token, ["invalid_hash_1", "invalid_hash_2"])
        assert response.status_code == 500
        delete_user(access_token)
