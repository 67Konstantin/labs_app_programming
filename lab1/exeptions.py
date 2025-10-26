from datetime import datetime
from classes import *


def test_exceptions():

    print("Тест создания класса с невалидными данными\n")

    try:
        user1 = User(
            userId=101001,
            firstName="Иван",
            lastName="Петров",
            description="Тест",
            avatarUrl="https://example.com/avatar.jpg",
            email="Привет всем! это мой влог",  # Невалидный email
            lastActive=datetime.now(),
        )
        print(f"   ✅ Пользователь создан: {user1.get_full_name()}")
    except Exception as e:
        print(f"   ❌ Ошибка: {type(e).__name__}: {e}")
    print("======================================\n")
    try:
        user2 = User(
            userId=104002,  # Невалидный ID
            firstName="Мария",
            lastName="Иванова",
            description="Тест",
            avatarUrl="https://example.com/avatar2.jpg",
            email="123@valid.com",
            lastActive=datetime.now(),
            followers={101404},
        )
        print(f"   ✅ Пользователь создан: {user2.get_full_name()}")
    except Exception as e:
        print(f"   ❌ Ошибка: {type(e).__name__}: {e}")

    print("======================================\n")
    try:
        user2 = User(
            userId="Это мой id",  # Невалидный ID
            firstName="Мария",
            lastName="Иванова",
            description="Тест",
            avatarUrl="https://example.com/avatar2.jpg",
            email="123@valid.com",
            lastActive=datetime.now(),
            followers={101404},
        )
        print(f"   ✅ Пользователь создан: {user2.get_full_name()}")
    except Exception as e:
        print(f"   ❌ Ошибка: {type(e).__name__}: {e}")

    print("======================================\n")
    try:
        user2 = User(
            userId=101002,
            firstName="Мария",
            lastName="Иванова",
            description="Тест",
            avatarUrl="https://example.com/avatar2.jpg",
            email="123@valid.com",
            lastActive=datetime.now(),
            followers={101404},
        )
        print(f"   ✅ Пользователь создан: {user2.get_full_name()}")
    except Exception as e:
        print(f"   ❌ Ошибка: {type(e).__name__}: {e}")


test_exceptions()
