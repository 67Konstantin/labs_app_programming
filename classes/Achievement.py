from datetime import datetime
from classes import *
from typing import Optional


class Achievement:
    achievementId: int
    title: str
    description: str
    iconUrl: str
    isUnlocked: bool
    unlockedAt: Optional[datetime]
    userId: Optional[int]


    def __init__(
        self,
        achievementId: int,
        title: str,
        description: str,
        iconUrl: str,
        isUnlocked: bool = False,
        unlockedAt: Optional[datetime] = None,
        userId: Optional[int] = None,
    ):
        if not isinstance(achievementId, int) or not str(achievementId).startswith("102"):
            raise TypeError("achievementId должен быть int и начинаться с 102.")
        self.achievementId = achievementId

        if not isinstance(title, str) or not title.strip():
            raise ValueError("title должен быть непустой строкой.")
        self.title = title

        if not isinstance(description, str):
            raise ValueError("description должен быть строкой.")
        self.description = description

        if not isinstance(iconUrl, str) or not (iconUrl.startswith("http://") or iconUrl.startswith("https://")):
            raise ValueError("Некорректный формат iconUrl (должен начинаться с http:// или https://).")
        self.iconUrl = iconUrl

        if not isinstance(isUnlocked, bool):
            raise TypeError("isUnlocked должен быть bool.")
        self.isUnlocked = isUnlocked

        if unlockedAt is not None and not isinstance(unlockedAt, datetime):
            raise TypeError("unlockedAt должен быть экземпляром datetime или None.")
        self.unlockedAt = unlockedAt

        if userId is not None and not isinstance(userId, int):
            raise TypeError("userId должен быть int или None.")
        self.userId = userId


    def unlock(self, userId: int) -> None:
        # Помечает достижение как открытое пользователем
        if not self.isUnlocked:
            self.isUnlocked = True
            self.unlockedAt = datetime.now()
            self.userId = userId

    def is_achieved(self) -> bool:
        # Проверяет, было ли достижение открыто
        return self.isUnlocked

    def assign_to_user(self, userId: int) -> None:
        # Привязывает достижение к пользователю (без открытия)
        self.userId = userId

    def printing(self) -> None:
        print(
            f"Achievement(achievementId={self.achievementId}, title='{self.title}', "
            f"description='{self.description}', iconUrl='{self.iconUrl}', "
            f"isUnlocked={self.isUnlocked}, unlockedAt={self.unlockedAt}, userId={self.userId})"
        )