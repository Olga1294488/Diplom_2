import pytest
import allure
from helpers.api_client import ApiClient
from helpers.generators import UserGenerator


@pytest.fixture
def unique_user():
    """Фикстура, создающая уникального пользователя и удаляющая его после теста."""
    user_data = UserGenerator.generate_unique_user()
    
    # Создаем пользователя
    with allure.step("Создать тестового пользователя"):
        client = ApiClient()
        response = client.post("/auth/register", data=user_data)
        user_data["access_token"] = response.json().get("accessToken", "")
    
    yield user_data
    
    # Удаляем пользователя после теста
    with allure.step("Очистка: удалить тестового пользователя"):
        if user_data.get("access_token"):
            headers = {"Authorization": user_data["access_token"]}
            client.delete("/auth/user", headers=headers)


@pytest.fixture
def authorized_client(unique_user):
    """Фикстура, возвращающая авторизованный API клиент."""
    client = ApiClient()
    if unique_user.get("access_token"):
        client.session.headers.update({"Authorization": unique_user["access_token"]})
    return client