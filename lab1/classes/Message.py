from datetime import datetime
from typing import List, Optional


class Message:
    messageId: int
    chatId: int
    userId: int
    text: str
    mediaUrls: str
    timeSent: datetime
    isRead: bool
    isEdited: bool
    isDeleted: bool

    def __init__(
        self,
        messageId: int,
        chatId: int,
        userId: int,
        text: str,
        mediaUrls: Optional[List[str]] = None,
        timeSent: Optional[datetime] = None,
        isRead: bool = False,
        isEdited: bool = False,
        isDeleted: bool = False,
    ):
        if not isinstance(messageId, int) or not str(messageId).startswith("106"):
            raise TypeError("messageId должен быть int и начинаться с 106.")
        self.messageId = messageId

        if not isinstance(chatId, int) or not str(chatId).startswith("103"):
            raise TypeError("chatId должен быть int и начинаться с 103.")
        self.chatId = chatId

        if not isinstance(userId, int):
            raise TypeError("userId должен быть int.")
        self.userId = userId

        if not isinstance(text, str):
            raise ValueError("text должен быть строкой.")
        self.text = text

        if not isinstance(mediaUrls, (str, type(None))):
            raise TypeError("mediaUrls должен быть строкой или None.")
        self.mediaUrls = mediaUrls or None

        if timeSent is not None and not isinstance(timeSent, datetime):
            raise TypeError("timeSent должен быть экземпляром datetime или None.")
        self.timeSent = timeSent or datetime.now()

        if not isinstance(isRead, bool):
            raise TypeError("isRead должен быть bool.")
        self.isRead = isRead

        if not isinstance(isEdited, bool):
            raise TypeError("isEdited должен быть bool.")
        self.isEdited = isEdited

        if not isinstance(isDeleted, bool):
            raise TypeError("isDeleted должен быть bool.")
        self.isDeleted = isDeleted

    def edit(self, text: str) -> None:
        # Редактируем сообщение, если оно не удалено
        if not self.isDeleted:
            self.text = text
            self.isEdited = True

    def delete(self) -> None:
        # Помечаем сообщение как удалённое
        self.text = "[Сообщение удалено]"
        self.mediaUrls.clear()
        self.isDeleted = True

    def mark_as_read(self) -> None:
        # Помечаем сообщение как прочитанное
        self.isRead = True

    def printing(self) -> None:
        print(
            f"Message(messageId={self.messageId}, chatId={self.chatId}, userId={self.userId}, "
            f"text='{self.text[:50]}...', mediaUrls={len(self.mediaUrls)}, "
            f"timeSent={self.timeSent}, isRead={self.isRead}, "
            f"isEdited={self.isEdited}, isDeleted={self.isDeleted})"
        )