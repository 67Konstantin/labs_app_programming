from datetime import datetime
from typing import List, Set, Optional
from classes import *


class Story:
    storyId: int
    userId: int
    description: str
    mediaUrl: str
    viewersCount: int
    reactions: List["Reaction"]
    viewers: Set[int]
    timePublish: datetime
    isArchived: bool
    isDeleted: bool

    def __init__(
        self,
        storyId: int,
        userId: int,
        description: str,
        mediaUrl: str,
        viewersCount: int = 0,
        reactions: Optional[List["Reaction"]] = None,
        viewers: Optional[Set[int]] = None,
        timePublish: Optional[datetime] = None,
        isArchived: bool = False,
        isDeleted: bool = False,
    ):
        if not isinstance(storyId, int) or not str(storyId).startswith("110"):
            raise TypeError("storyId должен быть int и начинаться с 110.")
        self.storyId = storyId

        if not isinstance(userId, int):
            raise TypeError("userId должен быть int.")
        self.userId = userId

        if not isinstance(description, str):
            raise ValueError("description должен быть строкой.")
        self.description = description

        if not isinstance(mediaUrl, str) or not (mediaUrl.startswith("http://") or mediaUrl.startswith("https://")):
            raise ValueError("Некорректный формат mediaUrl (должен начинаться с http:// или https://).")
        self.mediaUrl = mediaUrl

        if not isinstance(viewersCount, int) or viewersCount < 0:
            raise ValueError("viewersCount должен быть неотрицательным int.")
        self.viewersCount = viewersCount

        if reactions is not None:
            if not isinstance(reactions, list):
                raise TypeError("reactions должен быть списком (list) или None.")
            for reaction in reactions:
                if not isinstance(reaction, Reaction):
                    raise TypeError("Все элементы reactions должны быть экземплярами Reaction.")
        self.reactions = reactions or []

        if viewers is not None:
            if not isinstance(viewers, set):
                raise TypeError("viewers должен быть множеством (set) или None.")
            for viewer in viewers:
                if not isinstance(viewer, int):
                    raise TypeError("Все элементы viewers должны быть int.")
        self.viewers = viewers or set()

        if timePublish is not None and not isinstance(timePublish, datetime):
            raise TypeError("timePublish должен быть экземпляром datetime или None.")
        self.timePublish = timePublish or datetime.now()

        if not isinstance(isArchived, bool):
            raise TypeError("isArchived должен быть bool.")
        self.isArchived = isArchived

        if not isinstance(isDeleted, bool):
            raise TypeError("isDeleted должен быть bool.")
        self.isDeleted = isDeleted


    def view(self, userId: int) -> None:
        # Отмечает просмотр истории пользователем
        if not self.isDeleted and userId not in self.viewers:
            self.viewers.add(userId)
            self.viewersCount += 1

    def get_viewers(self, users: List["User"]) -> List["User"]:
        # Возвращает список пользователей, просмотревших историю
        return [u for u in users if getattr(u, "userId", None) in self.viewers]

    def archive(self) -> None:
        # Архивирует историю
        if not self.isDeleted:
            self.isArchived = True

    def delete(self) -> None:
        # Удаляет историю
        self.isDeleted = True
        self.description = "[История удалена]"
        self.mediaUrl = ""
        self.reactions.clear()

    def get_reactions(self) -> List["Reaction"]:
        # Возвращает список реакций на историю
        return list(self.reactions)

    def add_reaction(self, reaction: "Reaction") -> None:
        # Добавляет реакцию к истории
        if not self.isDeleted:
            self.reactions.append(reaction)

    def printing(self) -> None:
        print(
            f"Story(storyId={self.storyId}, userId={self.userId}, "
            f"description='{self.description[:50]}...', mediaUrl='{self.mediaUrl}', "
            f"viewersCount={self.viewersCount}, reactions={len(self.reactions)}, "
            f"viewers={len(self.viewers)}, timePublish={self.timePublish}, "
            f"isArchived={self.isArchived}, isDeleted={self.isDeleted})"
        )