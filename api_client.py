import pytest
import requests
import allure
import random
import string
from urls import *

def generate_random_string(length):
    letters = string.ascii_lowercase
    random_string = ''.join(random.choice(letters) for i in range(length))
    return random_string

def create_new_user():
    name = generate_random_string(10)
    password = generate_random_string(10)
    email = f"{generate_random_string(8)}@test.com"
    payload = {
        "email": email,
        "password": password,
        "name": name
    }
    return payload


@allure.step('Удаление пользователя')
def delete_user(access_token):
    headers = {"Authorization": access_token}
    response = requests.delete(f"{BASE_URL}/auth/user", headers=headers)
    return response.status_code == 200


@allure.step('Создание и логин пользователя')
def create_and_login_user():
    payload = create_new_user()
    response = requests.post(f"{BASE_URL}/auth/register", json=payload)
    if response.status_code == 200:
        access_token = response.json().get("accessToken")
        return payload, access_token
    else:
        raise Exception(f"Не удалось создать пользователя: {response.text}")
    

    
@allure.step('Получение данных пользователя')
def get_user_info(access_token):
    headers = {"Authorization": access_token}
    response = requests.get(f"{BASE_URL}/auth/user", headers=headers)
    return response


@allure.step('Обновление данных пользователя')
def update_user_info(access_token, update_data):
    headers = {"Authorization": access_token}
    response = requests.patch(f"{BASE_URL}/auth/user", headers=headers, json=update_data)
    return response


@allure.step('Создание заказа')
def create_order(access_token=None, ingredients=None):
    headers = {}
    if access_token:
        headers["Authorization"] = access_token
    payload = {}
    if ingredients is not None:
        payload["ingredients"] = ingredients
    
    response = requests.post(f"{BASE_URL}/orders", headers=headers, json=payload)
    return response


@allure.step('Получение заказов пользователя')
def get_user_orders(access_token):
    headers = {"Authorization": access_token}
    response = requests.get(f"{BASE_URL}/orders", headers=headers)
    return response


@allure.step('Получение списка ингредиентов')
def get_ingredients():
    response = requests.get(f"{BASE_URL}/ingredients")
    return response


def get_valid_ingredient_ids(count=2):
    response = get_ingredients()
    if response.status_code == 200:
        ingredients_data = response.json()
        # Берем первые N валидных ингредиентов
        valid_ingredients = [ingredient["_id"] for ingredient in ingredients_data.get("data", [])[:count]]
        return valid_ingredients
    return None

@allure.step('Получение заказов пользователя')
def get_user_orders(access_token):
    headers = {}
    if access_token:
        headers["Authorization"] = access_token
    
    response = requests.get(f"{BASE_URL}/orders", headers=headers)
    return response
