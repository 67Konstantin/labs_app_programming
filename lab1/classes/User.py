from datetime import datetime
from typing import List, Set
from classes import *
from custom_exceptions import *


class User:
    userId: int
    firstName: str
    lastName: str
    description: str
    avatarUrl: str
    email: str
    lastActive: datetime
    achievements: List["Achievement"]
    followers: Set[int]
    following: Set[int]

    def __init__(
        self,
        userId: int,
        firstName: str,
        lastName: str,
        description: str,
        avatarUrl: str,
        email: str,
        lastActive: datetime,
        achievements: List["Achievement"] | None = None,
        followers: Set[int] | None = None,
        following: Set[int] | None = None,
    ):
        if not isinstance(userId, int):
            raise ValueError("userId должен быть целым числом")

        if not str(userId).startswith("101"):
            raise InvalidUserIdException(userId)
        self.userId = userId

        if not isinstance(firstName, str) and firstName.strip():
            raise ValueError("firstName должен быть непустой строкой.")
        self.firstName = firstName

        if not isinstance(lastName, str) and lastName.strip():
            raise ValueError("lastName должен быть непустой строкой.")
        self.lastName = lastName

        if not isinstance(description, str):
            raise ValueError("description должен быть строкой.")
        self.description = description

        if not isinstance(avatarUrl, str) or not (
            avatarUrl.startswith("http://") or avatarUrl.startswith("https://")
        ):
            raise ValueError(
                "Некорректный формат avatarUrl (должен начинаться с http:// или https://)."
            )
        self.avatarUrl = avatarUrl

        if (
            not isinstance(email, str)
            or "@" not in email
            or "." not in email.split("@")[-1]
        ):
            raise InvalidEmailException(email)
        self.email = email

        if not isinstance(lastActive, datetime):
            raise TypeError("lastActive должен быть экземпляром datetime.")
        self.lastActive = lastActive

        if achievements is not None:
            if not isinstance(achievements, list):
                raise TypeError("achievements должен быть списком (list) или None.")
            for ach in achievements:
                if not isinstance(ach, Achievement):
                    raise TypeError(
                        "Все элементы achievements должны быть экземплярами Achievement."
                    )
        self.achievements = achievements or []

        if followers is not None:
            if not isinstance(followers, set):
                raise TypeError("followers должен быть множеством (set) или None.")
            for f in followers:
                if not isinstance(f, int):
                    raise TypeError(
                        "Все элементы followers должны быть экземплярами int."
                    )
        self.followers = followers or set()

        if following is not None:
            if not isinstance(following, set):
                raise TypeError("following должен быть множеством (set) или None.")
            for u in following:
                if not isinstance(u, int):
                    raise TypeError(
                        "Все элементы following должны быть экземплярами int."
                    )
        self.following = following or set()

    def get_full_name(self) -> str:
        # Получение полного имени пользователя
        return f"{self.firstName} {self.lastName}"

    def get_followers(self) -> List[int]:
        # Получение списка ID подписчиков
        return list(self.followers)

    def get_following(self) -> List[int]:
        # Получение списка ID пользователей, на которых подписан
        return list(self.following)

    def get_achievements(self) -> List["Achievement"]:
        # Получение списка достижений пользователя
        return list(self.achievements)

    def update_profile(
        self, description: str | None = None, avatarUrl: str | None = None
    ) -> None:
        # Обновление описания и аватара пользователя
        if description is not None:
            self.description = description
        if avatarUrl is not None:
            self.avatarUrl = avatarUrl
        self.lastActive = datetime.now()

    def follow(self, user_id: int) -> None:
        # Подписаться на пользователя по ID
        if user_id == self.userId:
            return  # Не могу подписаться на самого себя
        self.following.add(user_id)

    def unfollow(self, user_id: int) -> None:
        # Отписаться от пользователя по ID
        self.following.discard(user_id)

    def add_follower(self, user_id: int) -> None:
        # Добавить подписчика (используется при импорте или связывании)
        if user_id != self.userId:
            self.followers.add(user_id)

    def add_achievement(self, achievement: "Achievement") -> None:
        # Добавить достижение пользователю, если его ещё нет
        if achievement not in self.achievements:
            self.achievements.append(achievement)

    def printing(self) -> None:
        print(
            f"User(userId={self.userId}, firstName='{self.firstName}', lastName='{self.lastName}', "
            f"description='{self.description}', avatarUrl='{self.avatarUrl}', "
            f"email='{self.email}', lastActive={self.lastActive}, "
            f"achievements={len(self.achievements)}, followers={len(self.followers)}, following={len(self.following)})"
        )
