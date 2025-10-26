from datetime import datetime
from typing import Optional


class Notification:
    notificationId: int
    userId: int
    text: str
    clickUrl: str
    timePublish: datetime
    isRead: bool
    isOpened: bool

    def __init__(
        self,
        notificationId: int,
        userId: int,
        text: str,
        clickUrl: str,
        timePublish: Optional[datetime] = None,
        isRead: bool = False,
        isOpened: bool = False,
    ):
        if not isinstance(notificationId, int) or not str(notificationId).startswith("107"):
            raise TypeError("notificationId должен быть int и начинаться с 107.")
        self.notificationId = notificationId

        if not isinstance(userId, int):
            raise TypeError("userId должен быть int.")
        self.userId = userId

        if not isinstance(text, str):
            raise ValueError("text должен быть строкой.")
        self.text = text

        if not isinstance(clickUrl, str) or not (clickUrl.startswith("http://") or clickUrl.startswith("https://")):
            raise ValueError("Некорректный формат clickUrl (должен начинаться с http:// или https://).")
        self.clickUrl = clickUrl

        if timePublish is not None and not isinstance(timePublish, datetime):
            raise TypeError("timePublish должен быть экземпляром datetime или None.")
        self.timePublish = timePublish or datetime.now()

        if not isinstance(isRead, bool):
            raise TypeError("isRead должен быть bool.")
        self.isRead = isRead

        if not isinstance(isOpened, bool):
            raise TypeError("isOpened должен быть bool.")
        self.isOpened = isOpened

    def mark_as_read(self) -> None:
        # Помечаем уведомление как прочитанное
        self.isRead = True

    def open(self) -> None:
        # Открываем уведомление и помечаем как прочитанное
        self.isOpened = True
        self.isRead = True

    def printing(self) -> None:
        print(
            f"Notification(notificationId={self.notificationId}, userId={self.userId}, "
            f"text='{self.text[:50]}...', clickUrl='{self.clickUrl}', "
            f"timePublish={self.timePublish}, isRead={self.isRead}, isOpened={self.isOpened})"
        )