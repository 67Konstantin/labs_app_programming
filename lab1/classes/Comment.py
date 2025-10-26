from datetime import datetime
from typing import List, Optional, Set
from classes import *


class Comment:
    commentId: int
    userId: int
    text: str
    mediaUrls: str
    likesCount: int
    answerTo: Optional[int]
    timePublish: datetime
    isDeleted: bool
    likedBy: Set[int]
    replies: List["Comment"]

    def __init__(
        self,
        commentId: int,
        userId: int,
        text: str,
        likesCount: int,
        timePublish: datetime,
        mediaUrls: Optional[List[str]] = None,
        answerTo: Optional[int] = None,
        likedBy: Optional[Set[int]] = None,
        isDeleted: bool = False,
        replies: Optional[List["Comment"]] = None,
    ):
        if not isinstance(commentId, int) or not str(commentId).startswith("104"):
            raise TypeError("commentId должен быть int и начинаться с 104.")
        self.commentId = commentId

        if not isinstance(userId, int):
            raise TypeError("userId должен быть int.")
        self.userId = userId

        if not isinstance(text, str):
            raise ValueError("text должен быть строкой.")
        self.text = text

        if not isinstance(likesCount, int) or likesCount < 0:
            raise ValueError("likesCount должен быть неотрицательным int.")
        self.likesCount = likesCount

        if not isinstance(timePublish, datetime):
            raise TypeError("timePublish должен быть экземпляром datetime.")
        self.timePublish = timePublish

        if not isinstance(mediaUrls, (str, type(None))):
            raise TypeError("mediaUrls должен быть строкой или None.")
        self.mediaUrls = mediaUrls or None

        if not isinstance(answerTo, (int, None)):
            raise TypeError("answerTo должен быть int или None.")
        self.answerTo = answerTo or None

        if likedBy is not None and not isinstance(likedBy, set):
            raise TypeError("likedBy должен быть множеством (set) или None.")
        self.likedBy = likedBy or set()

        if not isinstance(isDeleted, bool):
            raise TypeError("isDeleted должен быть bool.")
        self.isDeleted = isDeleted

        if replies is not None and not isinstance(replies, list):
            raise TypeError("replies должен быть списком (list) или None.")
        self.replies = replies or []


    def like(self, userId: int) -> None:
        # Лайкаем
        if not self.isDeleted and userId not in self.likedBy:
            self.likedBy.add(userId)
            self.likesCount += 1

    def unlike(self, userId: int) -> None:
        # Убираем лайк от пользователя
        if userId in self.likedBy:
            self.likedBy.remove(userId)
            self.likesCount = max(0, self.likesCount - 1)

    def edit(self, text: str) -> None:
        # Изменяем текст комментария, если он не удалён
        if not self.isDeleted:
            self.text = text

    def delete(self) -> None:
        # Удаляем комментарий, заменяя текст на placeholder
        self.text = "[Комментарий удалён]"
        self.mediaUrls.clear()
        self.isDeleted = True

    def add_reply(self, reply: "Comment") -> None:
        # Добавляем ответ на комментарий
        self.replies.append(reply)

    def get_replies(self) -> List["Comment"]:
        # Получаем список ответов
        return list(self.replies)

    def printing(self) -> None:
        print(
            f"Comment(commentId={self.commentId}, userId={self.userId}, text='{self.text[:50]}...', "
            f"mediaUrls={len(self.mediaUrls)}, likesCount={self.likesCount}, "
            f"answerTo={self.answerTo}, timePublish={self.timePublish}, "
            f"isDeleted={self.isDeleted}, replies={len(self.replies)})"
        )