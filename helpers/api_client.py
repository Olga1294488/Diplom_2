import requests
import allure
from config.config import BASE_URL


class ApiClient:
    """Базовый клиент для работы с API Stellar Burgers."""
    
    def __init__(self):
        self.base_url = BASE_URL
        self.session = requests.Session()
    
    @allure.step("Отправить {method} запрос на {endpoint}")
    def _request(self, method, endpoint, data=None, headers=None):
        url = f"{self.base_url}{endpoint}"
        
        with allure.step(f"Параметры запроса: URL={url}, data={data}"):
            response = self.session.request(
                method=method,
                url=url,
                json=data,
                headers=headers
            )
        
        # Логируем ответ как текст, чтобы избежать JSONDecodeError при не-JSON ответах
        with allure.step(f"Ответ сервера: status={response.status_code}, body={response.text}"):
            return response
    
    def get(self, endpoint, headers=None):
        return self._request("GET", endpoint, headers=headers)
    
    def post(self, endpoint, data=None, headers=None):
        return self._request("POST", endpoint, data=data, headers=headers)
    
    def patch(self, endpoint, data=None, headers=None):
        return self._request("PATCH", endpoint, data=data, headers=headers)
    
    def delete(self, endpoint, headers=None):
        return self._request("DELETE", endpoint, headers=headers)