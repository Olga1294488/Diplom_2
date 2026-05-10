import allure
import pytest
from helpers.api_client import ApiClient
from config.config import REGISTER_ENDPOINT
from config.error_messages import USER_ALREADY_EXISTS, MISSING_FIELD_ERROR
from helpers.generators import UserGenerator


@allure.epic("Stellar Burgers API")
@allure.feature("Создание пользователя")
class TestUserRegistration:
    
    @allure.title("Создание уникального пользователя")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_unique_user(self):
        client = ApiClient()
        user_data = UserGenerator.generate_unique_user()
        
        with allure.step("Отправить запрос на регистрацию нового пользователя"):
            response = client.post(REGISTER_ENDPOINT, data=user_data)
        
        with allure.step("Проверить ответ сервера"):
            assert response.status_code == 200
            response_data = response.json()
            assert response_data["success"] is True
            assert "accessToken" in response_data
            assert "refreshToken" in response_data
            assert response_data["user"]["email"] == user_data["email"]
            assert response_data["user"]["name"] == user_data["name"]
        
        # Очистка
        access_token = response_data.get("accessToken")
        if access_token:
            with allure.step("Удалить созданного пользователя"):
                headers = {"Authorization": access_token}
                client.delete("/auth/user", headers=headers)
    
    @allure.title("Создание пользователя, который уже зарегистрирован")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_existing_user(self, unique_user):
        client = ApiClient()
        user_data = {
            "email": unique_user["email"],
            "password": unique_user["password"],
            "name": unique_user["name"]
        }
        
        with allure.step("Повторно отправить запрос на регистрацию того же пользователя"):
            response = client.post(REGISTER_ENDPOINT, data=user_data)
        
        with allure.step("Проверить, что сервер возвращает ошибку"):
            assert response.status_code == 403
            response_data = response.json()
            assert response_data["success"] is False
            assert response_data["message"] == USER_ALREADY_EXISTS
    
    @allure.title("Создание пользователя без заполнения обязательного поля")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("missing_field", ["email", "password", "name"])
    def test_create_user_missing_field(self, missing_field):
        client = ApiClient()
        user_data = UserGenerator.generate_user_with_missing_field(missing_field)
        
        with allure.step(f"Отправить запрос без поля '{missing_field}'"):
            response = client.post(REGISTER_ENDPOINT, data=user_data)
        
        with allure.step("Проверить, что сервер возвращает ошибку валидации"):
            assert response.status_code == 403
            response_data = response.json()
            assert response_data["success"] is False
            assert response_data["message"] == MISSING_FIELD_ERROR