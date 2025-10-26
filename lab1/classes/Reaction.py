from datetime import datetime
from typing import List, Optional
from classes import *


class Reaction:
    reactionId: int
    userId: int
    type: str
    createdAt: datetime
    isRemoved: bool

    def __init__(
        self,
        reactionId: int,
        userId: int,
        reactionType: str,
        createdAt: Optional[datetime] = None,
        isRemoved: bool = False,
    ):
        if not isinstance(reactionId, int) or not str(reactionId).startswith("108"):
            raise TypeError("reactionId должен быть int и начинаться с 108.")
        self.reactionId = reactionId

        if not isinstance(userId, int):
            raise TypeError("userId должен быть int.")
        self.userId = userId

        if not isinstance(reactionType, str) or not reactionType.strip():
            raise ValueError("reactionType должен быть непустой строкой.")
        self.type = reactionType

        if createdAt is not None and not isinstance(createdAt, datetime):
            raise TypeError("createdAt должен быть экземпляром datetime или None.")
        self.createdAt = createdAt or datetime.now()

        if not isinstance(isRemoved, bool):
            raise TypeError("isRemoved должен быть bool.")
        self.isRemoved = isRemoved

    def change_type(self, newType: str) -> None:
        # Изменяем тип реакции (например, с "Сердце" на "Класс")
        if not self.isRemoved:
            self.type = newType

    def remove(self) -> None:
        # Удаляем реакцию
        self.isRemoved = True

    def get_user(self, users: List["User"]) -> Optional["User"]:
        # Получаем объект пользователя по userId
        for user in users:
            if getattr(user, "userId", None) == self.userId:
                return user
        return None

    def printing(self) -> None:
        print(
            f"Reaction(reactionId={self.reactionId}, userId={self.userId}, "
            f"type='{self.type}', createdAt={self.createdAt}, isRemoved={self.isRemoved})"
        )