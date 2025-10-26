from datetime import datetime
from typing import List, Optional
from classes import *


class MarketplaceItem:
    itemId: int
    title: str
    description: str
    photoUrls: str
    sellerId: int
    price: float
    status: str  # active или sold
    createdAt: datetime

    def __init__(
        self,
        itemId: int,
        title: str,
        description: str,
        photoUrls: Optional[List[str]] = None,
        sellerId: int = 0,
        price: float = 0.0,
        status: str = "active",
        createdAt: Optional[datetime] = None,
    ):
        if not isinstance(itemId, int) or not str(itemId).startswith("105"):
            raise TypeError("itemId должен быть int и начинаться с 105.")
        self.itemId = itemId

        if not isinstance(title, str) or not title.strip():
            raise ValueError("title должен быть непустой строкой.")
        self.title = title

        if not isinstance(description, str):
            raise ValueError("description должен быть строкой.")
        self.description = description

        if not isinstance(photoUrls, (str, type(None))):
            raise TypeError("photoUrls должен быть строкой или None.")
        self.mediaUrls = photoUrls or None

        if not isinstance(sellerId, int):
            raise TypeError("sellerId должен быть int.")
        self.sellerId = sellerId

        if not isinstance(price, (int, float)) or price < 0:
            raise ValueError("price должен быть неотрицательным числом.")
        self.price = float(price)

        if not isinstance(status, str) or status not in ["active", "sold"]:
            raise ValueError("status должен быть 'active' или 'sold'.")
        self.status = status

        if createdAt is not None and not isinstance(createdAt, datetime):
            raise TypeError("createdAt должен быть экземпляром datetime или None.")
        self.createdAt = createdAt or datetime.now()

    def mark_as_sold(self) -> None:
        # Помечаем товар как проданный
        if self.status != "sold":
            self.status = "sold"

    def add_photo(self, photoUrl: str) -> None:
        # Добавляем новую фотографию товара
        self.photoUrls.append(photoUrl)

    def update_price(self, newPrice: float) -> None:
        # Обновляем цену, если она положительная
        if newPrice > 0:
            self.price = newPrice

    def get_seller(self, users: List["User"]) -> Optional["User"]:
        # Получаем объект пользователя по sellerId, если он есть в списке
        for user in users:
            if getattr(user, "userId", None) == self.sellerId:
                return user
        return None

    def printing(self) -> None:
        print(
            f"MarketplaceItem(itemId={self.itemId}, title='{self.title}', "
            f"description='{self.description[:50]}...', photoUrls={len(self.photoUrls)}, "
            f"sellerId={self.sellerId}, price={self.price}, status='{self.status}', "
            f"createdAt={self.createdAt})"
        )