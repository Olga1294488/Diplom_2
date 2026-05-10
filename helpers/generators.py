import time
import random
from faker import Faker

fake = Faker()


class UserGenerator:
    @staticmethod
    def generate_unique_user():
        unique_suffix = f"{int(time.time() * 1000)}_{random.randint(1000, 9999)}"
        return {
            "email": f"{fake.user_name()}_{unique_suffix}@test.com",
            "password": fake.password(length=8),
            "name": fake.name()
        }

    @staticmethod
    def generate_user_with_missing_field(missing_field):
        full_user = UserGenerator.generate_unique_user()
        if missing_field in full_user:
            del full_user[missing_field]
        return full_user

    @staticmethod
    def generate_invalid_credentials():
        return {
            "email": fake.email(),
            "password": "wrong_password_123"
        }


class OrderGenerator:
    @staticmethod
    def generate_order_with_ingredients(ingredients_list):
        return {"ingredients": ingredients_list}