import allure
from helpers.api_client import ApiClient
from config.config import LOGIN_ENDPOINT
from config.error_messages import INCORRECT_CREDENTIALS
from helpers.generators import UserGenerator


@allure.epic("Stellar Burgers API")
@allure.feature("Логин пользователя")
class TestUserLogin:
    
    @allure.title("Вход под существующим пользователем")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_login_existing_user(self, unique_user):
        client = ApiClient()
        login_data = {
            "email": unique_user["email"],
            "password": unique_user["password"]
        }
        
        with allure.step("Отправить запрос на логин с корректными данными"):
            response = client.post(LOGIN_ENDPOINT, data=login_data)
        
        with allure.step("Проверить успешный ответ сервера"):
            assert response.status_code == 200
            response_data = response.json()
            assert response_data["success"] is True
            assert "accessToken" in response_data
            assert "refreshToken" in response_data
            assert response_data["user"]["email"] == unique_user["email"]
            assert response_data["user"]["name"] == unique_user["name"]
    
    @allure.title("Вход с неверным логином и паролем")
    @allure.severity(allure.severity_level.NORMAL)
    def test_login_with_invalid_credentials(self):
        client = ApiClient()
        invalid_data = UserGenerator.generate_invalid_credentials()
        
        with allure.step("Отправить запрос на логин с неверными данными"):
            response = client.post(LOGIN_ENDPOINT, data=invalid_data)
        
        with allure.step("Проверить, что сервер возвращает ошибку авторизации"):
            assert response.status_code == 401
            response_data = response.json()
            assert response_data["success"] is False
            assert response_data["message"] == INCORRECT_CREDENTIALS