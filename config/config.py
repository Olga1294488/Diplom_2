BASE_URL = "https://stellarburgers.education-services.ru/api"

# Эндпоинты
REGISTER_ENDPOINT = "/auth/register"
LOGIN_ENDPOINT = "/auth/login"
ORDERS_ENDPOINT = "/orders"
USER_ENDPOINT = "/auth/user"

# Тестовые ингредиенты
VALID_INGREDIENTS = [
    "61c0c5a71d1f82001bdaaa6d",  # Bun
    "61c0c5a71d1f82001bdaaa6f"   # Sauce
]
INVALID_INGREDIENTS_HASH = "invalid_hash_12345"
EMPTY_INGREDIENTS = []