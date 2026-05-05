import allure
import pytest
from helpers.api_client import ApiClient
from config.config import ORDERS_ENDPOINT, VALID_INGREDIENTS, INVALID_INGREDIENTS_HASH, EMPTY_INGREDIENTS
from config.error_messages import INGREDIENT_IDS_MISSING
from helpers.generators import OrderGenerator


@allure.epic("Stellar Burgers API")
@allure.feature("Создание заказа")
class TestCreateOrder:
    
    @allure.title("Создание заказа с авторизацией и ингредиентами")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_order_with_auth_and_ingredients(self, authorized_client):
        order_data = OrderGenerator.generate_order_with_ingredients(VALID_INGREDIENTS)
        
        with allure.step("Отправить запрос на создание заказа (авторизованный пользователь)"):
            response = authorized_client.post(ORDERS_ENDPOINT, data=order_data)
        
        with allure.step("Проверить успешное создание заказа"):
            assert response.status_code == 200
            response_data = response.json()
            assert response_data["success"] is True
            assert "order" in response_data
            assert "number" in response_data["order"]
    
    @allure.title("Создание заказа без авторизации, но с ингредиентами")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_order_without_auth_with_ingredients(self):
        client = ApiClient()
        order_data = OrderGenerator.generate_order_with_ingredients(VALID_INGREDIENTS)
        
        with allure.step("Отправить запрос на создание заказа (неавторизованный пользователь)"):
            response = client.post(ORDERS_ENDPOINT, data=order_data)
        
        with allure.step("Проверить успешное создание заказа (заказы могут создаваться без авторизации)"):
            assert response.status_code == 200
            response_data = response.json()
            assert response_data["success"] is True
    
    @allure.title("Создание заказа с ингредиентами")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_order_with_ingredients(self, authorized_client):
        order_data = OrderGenerator.generate_order_with_ingredients(VALID_INGREDIENTS)
        
        with allure.step("Отправить запрос с валидными ингредиентами"):
            response = authorized_client.post(ORDERS_ENDPOINT, data=order_data)
        
        with allure.step("Проверить успешный ответ сервера"):
            assert response.status_code == 200
            assert response.json()["success"] is True
    
    @allure.title("Создание заказа без ингредиентов")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_order_without_ingredients(self, authorized_client):
        order_data = OrderGenerator.generate_order_with_ingredients(EMPTY_INGREDIENTS)
        
        with allure.step("Отправить запрос с пустым списком ингредиентов"):
            response = authorized_client.post(ORDERS_ENDPOINT, data=order_data)
        
        with allure.step("Проверить, что сервер возвращает ошибку"):
            assert response.status_code == 400
            response_data = response.json()
            assert response_data["success"] is False
            assert response_data["message"] == INGREDIENT_IDS_MISSING
    
    @allure.title("Создание заказа с неверным хешем ингредиентов")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_order_with_invalid_ingredients_hash(self, authorized_client):
        order_data = OrderGenerator.generate_order_with_ingredients([INVALID_INGREDIENTS_HASH])
        
        with allure.step("Отправить запрос с неверными идентификаторами ингредиентов"):
            response = authorized_client.post(ORDERS_ENDPOINT, data=order_data)
        
        with allure.step("Проверить, что сервер возвращает ошибку 500"):
            assert response.status_code == 500