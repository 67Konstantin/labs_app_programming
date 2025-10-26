from datetime import datetime
from classes import *
from typing import List, Optional


class Chat:
    chatId: int
    usersId: List[int]
    createdAt: datetime
    avatarUrl: str
    title: str
    _messages: List["Message"]
    _messageCounter: int

    def __init__(
        self,
        chatId: int,
        usersId: List[int],
        avatarUrl: str,
        title: str,
        createdAt: Optional[datetime] = None,
        messages: Optional[List["Message"]] = None,
    ):
        if not isinstance(chatId, int) or not str(chatId).startswith("103"):
            raise TypeError("chatId должен быть int и начинаться с 103.")
        self.chatId = chatId

        if not isinstance(usersId, list):
            raise TypeError("usersId должен быть списком (list).")
        for user_id in usersId:
            if not isinstance(user_id, int):
                raise TypeError("Все элементы usersId должны быть int.")
        self.usersId = usersId[:]

        if not isinstance(avatarUrl, str) or not (avatarUrl.startswith("http://") or avatarUrl.startswith("https://")):
            raise ValueError("Некорректный формат avatarUrl (должен начинаться с http:// или https://).")
        self.avatarUrl = avatarUrl

        if not isinstance(title, str) or not title.strip():
            raise ValueError("title должен быть непустой строкой.")
        self.title = title

        if createdAt is not None and not isinstance(createdAt, datetime):
            raise TypeError("createdAt должен быть экземпляром datetime или None.")
        self.createdAt = createdAt or datetime.now()

        if messages is not None and not isinstance(messages, list):
            raise TypeError("messages должен быть списком (list) или None.")
        self._messages = messages or []
        self._messageCounter = len(self._messages)

    def add_user(self, userId: int) -> None:
        # Добавляем пользователя в чат
        if userId not in self.usersId:
            self.usersId.append(userId)

    def remove_user(self, userId: int) -> None:
        # удаляем пользователя из чата
        if userId in self.usersId:
            self.usersId.remove(userId)

    def send_message(self, userId: int, text: str, mediaUrls: Optional[List[str]] = None) -> "Message":
        # Отправляем сообщение
        if userId not in self.usersId:
            raise ValueError(f"Ошибка: пользователь {userId} не состоит в чате {self.chatId}")

        self._messageCounter += 1
        msg = Message(
            messageId=self._messageCounter,
            chatId=self.chatId,
            userId=userId,
            text=text,
            mediaUrls=mediaUrls or [],
            timeSent=datetime.now(),
            isRead=False,
            isEdited=False,
            isDeleted=False,
        )
        self._messages.append(msg)
        return msg

    def get_messages(self) -> List["Message"]:
        # Получаем все сообщения 
        return list(self._messages)

    def printing(self) -> None:
        print(
            f"Chat(chatId={self.chatId}, usersId={self.usersId}, "
            f"avatarUrl='{self.avatarUrl}', title='{self.title}', "
            f"createdAt={self.createdAt}, messages={len(self._messages)})"
        )