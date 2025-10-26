from datetime import datetime
from typing import List, Optional, Set


class Post:
    postId: int
    userId: int
    text: str
    mediaUrls: str
    likesCount: int
    repostsCount: int
    comments: List[int]
    timePublish: datetime
    isDeleted: bool
    likedBy: Set[int]

    def __init__(
        self,
        postId: int,
        userId: int,
        text: str,
        mediaUrls: Optional[List[str]] = None,
        likesCount: int = 0,
        repostsCount: int = 0,
        comments: Optional[List[int]] = None,
        timePublish: Optional[datetime] = None,
        likedBy: Optional[Set[int]] = None,
        isDeleted: bool = False,
    ):
        if not isinstance(postId, int) or not str(postId).startswith("109"):
            raise TypeError("postId должен быть int и начинаться с 109.")
        self.postId = postId

        if not isinstance(userId, int):
            raise TypeError("userId должен быть int.")
        self.userId = userId

        if not isinstance(text, str):
            raise ValueError("text должен быть строкой.")
        self.text = text

        if not isinstance(mediaUrls, (str, type(None))):
            raise TypeError("mediaUrls должен быть строкой или None.")
        self.mediaUrls = mediaUrls or None

        if not isinstance(likesCount, int) or likesCount < 0:
            raise ValueError("likesCount должен быть неотрицательным int.")
        self.likesCount = likesCount

        if not isinstance(repostsCount, int) or repostsCount < 0:
            raise ValueError("repostsCount должен быть неотрицательным int.")
        self.repostsCount = repostsCount

        if comments is not None and not isinstance(comments, list):
            raise TypeError("comments должен быть списком (list) или None.")
        self.comments = comments or []

        if timePublish is not None and not isinstance(timePublish, datetime):
            raise TypeError("timePublish должен быть экземпляром datetime или None.")
        self.timePublish = timePublish or datetime.now()

        if likedBy is not None and not isinstance(likedBy, set):
            raise TypeError("likedBy должен быть множеством (set) или None.")
        self.likedBy = likedBy or set()

        if not isinstance(isDeleted, bool):
            raise TypeError("isDeleted должен быть bool.")
        self.isDeleted = isDeleted


    def like(self, userId: int) -> None:
        # Добавляем лайк, если пост не удалён
        if not self.isDeleted and userId not in self.likedBy:
            self.likedBy.add(userId)
            self.likesCount += 1

    def unlike(self, userId: int) -> None:
        # Убираем лайк
        if userId in self.likedBy:
            self.likedBy.remove(userId)
            self.likesCount = max(0, self.likesCount - 1)

    def add_comment(self, commentId: int) -> None:
        # Добавляем комментарий (по ID)
        if not self.isDeleted:
            self.comments.append(commentId)

    def share(self, userId: int) -> None:
        # Увеличиваем счётчик репостов
        if not self.isDeleted:
            self.repostsCount += 1

    def edit(self, text: str, mediaUrls: Optional[List[str]] = None) -> None:
        # Редактируем текст и медиа, если пост не удалён
        if not self.isDeleted:
            self.text = text
            if mediaUrls is not None:
                self.mediaUrls = mediaUrls

    def delete(self) -> None:
        # Удаляем пост
        self.text = "[Пост удалён]"
        self.mediaUrls.clear()
        self.isDeleted = True

    def printing(self) -> None:
        print(
            f"Post(postId={self.postId}, userId={self.userId}, text='{self.text[:50]}...', "
            f"mediaUrls={len(self.mediaUrls)}, likesCount={self.likesCount}, "
            f"repostsCount={self.repostsCount}, comments={len(self.comments)}, "
            f"timePublish={self.timePublish}, isDeleted={self.isDeleted})"
        )