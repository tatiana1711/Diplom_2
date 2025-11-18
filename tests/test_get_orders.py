import pytest
import allure
from api_client import *

class TestGetOrders:

    @allure.title('Получение заказов авторизованного пользователя')
    @allure.description('Получение списка заказов авторизованного пользователя. Ожидается статус 200 и наличие списка заказов в ответе')
    def test_get_orders_with_auth(self):
        user_data = create_and_login_user()
        access_token = user_data[1]
        response = get_user_orders(access_token)
        assert response.status_code == 200
        response_data = response.json()
        assert response_data["success"] is True
        assert "orders" in response_data
        delete_user(access_token)


    @allure.title('Ошибка получения заказов неавторизованного пользователя')
    @allure.description('Попытка получить заказы без авторизации. Ожидается ошибка 401 с сообщением о необходимости авторизации')
    def test_get_orders_without_auth(self):
        response = get_user_orders("")
        assert response.status_code == 401
        response_data = response.json()
        assert response_data["success"] is False
        assert "You should be authorised" in response_data["message"]