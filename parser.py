import json
from datetime import datetime
from typing import List, Optional
from classes import *
import xml.etree.ElementTree as ET


class Parser:

    def parser_xml(self, path: str = "lab1/data/data.xml") -> None:
        tree = ET.parse(path)
        root = tree.getroot()

        def parse_section(section_name: str, item_name: str):
            section = root.find(section_name)
            if section is None:
                return []
            result = []
            for item in section.findall(item_name):
                obj = {}
                for child in item:
                    tag = child.tag
                    text = child.text.strip() if child.text else None
                    
                    
                    if tag in ['achievements', 'followers', 'following', 'comments', 'likedBy', 
                              'mediaUrls', 'reactions', 'viewers', 'usersId', 'replies', 'photoUrls']:
                        # Всё для дочерних элементов
                        obj[tag] = []
                        for sub_item in child:
                            if sub_item.text and sub_item.text.strip():
                                obj[tag].append(sub_item.text.strip())
                    else:
                        if text == "None" or text == "":
                            obj[tag] = None
                        else:
                            obj[tag] = text
                result.append(obj)
            return result

        data = {
            "users": parse_section("users", "user"),
            "achievements": parse_section("achievements", "achievement"),
            "posts": parse_section("posts", "post"),
            "comments": parse_section("comments", "comment"),
            "reactions": parse_section("reactions", "reaction"),
            "messages": parse_section("messages", "message"),
            "chats": parse_section("chats", "chat"),
            "stories": parse_section("stories", "story"),
            "notifications": parse_section("notifications", "notification"),
            "marketplaceItems": parse_section("marketplaceItems", "marketplaceItem"),
        }

        # Преобразование типов данных
        for u in data["users"]:
            u["userId"] = int(u["userId"])
            u["followers"] = set(map(int, u.get("followers", [])))
            u["following"] = set(map(int, u.get("following", [])))

        for a in data["achievements"]:
            a["achievementId"] = int(a["achievementId"])
            a["isUnlocked"] = a["isUnlocked"].lower() == "true"
            a["userId"] = int(a["userId"]) if a.get("userId") and a["userId"] != "None" else None

        for p in data["posts"]:
            p["postId"] = int(p["postId"])
            p["userId"] = int(p["userId"])
            p["likesCount"] = int(p.get("likesCount", 0))
            p["repostsCount"] = int(p.get("repostsCount", 0))
            p["isDeleted"] = p.get("isDeleted", "false").lower() == "true"
            p["likedBy"] = set(map(int, p.get("likedBy", [])))
            p["comments"] = [int(x) for x in p.get("comments", [])]
            p["mediaUrls"] = p.get("mediaUrls", [])

        for c in data["comments"]:
            c["commentId"] = int(c["commentId"])
            c["userId"] = int(c["userId"])
            c["likesCount"] = int(c.get("likesCount", 0))
            c["isDeleted"] = c.get("isDeleted", "false").lower() == "true"
            c["likedBy"] = set(map(int, c.get("likedBy", [])))
            c["mediaUrls"] = c.get("mediaUrls", [])
            c["replies"] = c.get("replies", [])
            if "answerTo" in c and c["answerTo"] not in (None, ""):
                c["answerTo"] = int(c["answerTo"])
            else:
                c["answerTo"] = None

        for r in data["reactions"]:
            r["reactionId"] = int(r["reactionId"])
            r["userId"] = int(r["userId"])
            r["isRemoved"] = r.get("isRemoved", "false").lower() == "true"

        for m in data["messages"]:
            m["messageId"] = int(m["messageId"])
            m["chatId"] = int(m["chatId"])
            m["userId"] = int(m["userId"])
            m["mediaUrls"] = m.get("mediaUrls", [])
            for flag in ["isRead", "isEdited", "isDeleted"]:
                m[flag] = m.get(flag, "false").lower() == "true"

        for c in data["chats"]:
            c["chatId"] = int(c["chatId"])
            c["usersId"] = [int(x) for x in c.get("usersId", [])]

        for s in data["stories"]:
            s["storyId"] = int(s["storyId"])
            s["userId"] = int(s["userId"])
            s["viewersCount"] = int(s.get("viewersCount", 0))
            s["isArchived"] = s.get("isArchived", "false").lower() == "true"
            s["isDeleted"] = s.get("isDeleted", "false").lower() == "true"
            s["reactions"] = [int(x) for x in s.get("reactions", [])]
            s["viewers"] = set(map(int, s.get("viewers", [])))

        for n in data["notifications"]:
            n["notificationId"] = int(n["notificationId"])
            n["userId"] = int(n["userId"])
            n["isRead"] = n.get("isRead", "false").lower() == "true"
            n["isOpened"] = n.get("isOpened", "false").lower() == "true"

        for i in data["marketplaceItems"]:
            i["itemId"] = int(i["itemId"])
            i["sellerId"] = int(i["sellerId"])
            i["price"] = float(i["price"])
            i["photoUrls"] = i.get("photoUrls", [])
            i["createdAt"] = i["createdAt"]

        self.load_data(data)

    def parser_json(self, path: str = "lab1/data/data.json") -> None:
        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)

        self.load_data(data)

    def load_data(self, data):
        # Обработка медиа-URL для совместимости с классами
        for section in ("posts", "comments", "messages", "marketplaceItems"):
            for obj in data.get(section, []):
                key = "photoUrls" if section == "marketplaceItems" else "mediaUrls"
                value = obj.get(key, [])
                if isinstance(value, list):
                    obj[key] = ", ".join(str(v) for v in value) if value else ""
                elif value is None:
                    obj[key] = ""
                else:
                    obj[key] = str(value)

        self.users: List[User] = [
            User(
                userId=u["userId"],
                firstName=u["firstName"],
                lastName=u["lastName"],
                description=u["description"],
                avatarUrl=u["avatarUrl"],
                email=u["email"],
                lastActive=datetime.fromisoformat(u["lastActive"]),
                achievements=[],
                followers=set(u.get("followers", [])),
                following=set(u.get("following", [])),
            )
            for u in data["users"]
        ]

        self.achievements: List[Achievement] = [
            Achievement(
                achievementId=a["achievementId"],
                title=a["title"],
                description=a["description"],
                iconUrl=a["iconUrl"],
                isUnlocked=a["isUnlocked"],
                unlockedAt=(
                    datetime.fromisoformat(a["unlockedAt"])
                    if a.get("unlockedAt")
                    else None
                ),
                userId=a.get("userId"),
            )
            for a in data["achievements"]
        ]

        self.posts: List[Post] = [
            Post(
                postId=p["postId"],
                userId=p["userId"],
                text=p["text"],
                mediaUrls=p.get("mediaUrls", ""),
                likesCount=p.get("likesCount", 0),
                repostsCount=p.get("repostsCount", 0),
                comments=p.get("comments", []),
                likedBy=set(p.get("likedBy", [])),
                timePublish=datetime.fromisoformat(p["timePublish"]),
                isDeleted=p.get("isDeleted", False),
            )
            for p in data["posts"]
        ]

        self.comments: List[Comment] = [
            Comment(
                commentId=c["commentId"],
                userId=c["userId"],
                text=c["text"],
                mediaUrls=c.get("mediaUrls", ""),
                likesCount=c.get("likesCount", 0),
                answerTo=c.get("answerTo"),
                timePublish=datetime.fromisoformat(c["timePublish"]),
                isDeleted=c.get("isDeleted", False),
                likedBy=set(c.get("likedBy", [])),
                replies=c.get("replies", []),
            )
            for c in data["comments"]
        ]

        self.reactions: List[Reaction] = [
            Reaction(
                reactionId=r["reactionId"],
                userId=r["userId"],
                reactionType=r["type"],
                createdAt=datetime.fromisoformat(r["createdAt"]),
                isRemoved=r.get("isRemoved", False),
            )
            for r in data["reactions"]
        ]

        self.messages: List[Message] = [
            Message(
                messageId=m["messageId"],
                chatId=m["chatId"],
                userId=m["userId"],
                text=m["text"],
                mediaUrls=m.get("mediaUrls", ""),
                timeSent=datetime.fromisoformat(m["timeSent"]),
                isRead=m.get("isRead", False),
                isEdited=m.get("isEdited", False),
                isDeleted=m.get("isDeleted", False),
            )
            for m in data["messages"]
        ]

        self.chats: List[Chat] = [
            Chat(
                chatId=c["chatId"],
                usersId=c["usersId"],
                avatarUrl=c["avatarUrl"],
                title=c["title"],
                createdAt=datetime.fromisoformat(c["createdAt"]),
            )
            for c in data["chats"]
        ]

        self.stories: List[Story] = [
            Story(
                storyId=s["storyId"],
                userId=s["userId"],
                description=s["description"],
                mediaUrl=s["mediaUrl"],
                viewersCount=s.get("viewersCount", 0),
                reactions=[
                    r for r in self.reactions 
                    if r.reactionId in s.get("reactions", [])
                ],
                viewers=set(s.get("viewers", [])),
                timePublish=datetime.fromisoformat(s["timePublish"]),
                isArchived=s.get("isArchived", False),
                isDeleted=s.get("isDeleted", False),
            )
            for s in data["stories"]
        ]

        self.notifications: List[Notification] = [
            Notification(
                notificationId=n["notificationId"],
                userId=n["userId"],
                text=n["text"],
                clickUrl=n["clickUrl"],
                timePublish=datetime.fromisoformat(n["timePublish"]),
                isRead=n["isRead"],
                isOpened=n["isOpened"],
            )
            for n in data["notifications"]
        ]

        self.marketplaceItems: List[MarketplaceItem] = [
            MarketplaceItem(
                itemId=i["itemId"],
                title=i["title"],
                description=i["description"],
                photoUrls=i.get("photoUrls", ""),
                sellerId=i["sellerId"],
                price=i["price"],
                status=i["status"],
                createdAt=datetime.fromisoformat(i["createdAt"]),
            )
            for i in data["marketplaceItems"]
        ]

        print(
            f"Загружено: "
            f"{len(self.users)} пользователей, "
            f"{len(self.achievements)} достижений, "
            f"{len(self.posts)} постов, "
            f"{len(self.comments)} комментариев, "
            f"{len(self.reactions)} реакций, "
            f"{len(self.messages)} сообщений, "
            f"{len(self.chats)} чатов, "
            f"{len(self.stories)} историй, "
            f"{len(self.notifications)} уведомлений, "
            f"{len(self.marketplaceItems)} товаров."
        )

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        return next((u for u in self.users if u.userId == user_id), None)

    def get_posts_by_user(self, user_id: int) -> List[Post]:
        return [p for p in self.posts if p.userId == user_id]

    def get_comments_by_user(self, user_id: int) -> List[Comment]:
        return [c for c in self.comments if c.userId == user_id]

    def get_story_by_user(self, user_id: int) -> List[Story]:
        return [s for s in self.stories if s.userId == user_id]

    def get_reactions_by_user(self, user_id: int) -> List[Reaction]:
        return [r for r in self.reactions if r.userId == user_id]

    def get_messages_by_user(self, user_id: int) -> List[Message]:
        return [m for m in self.messages if m.userId == user_id]

    def get_chats_by_user(self, user_id: int) -> List[Chat]:
        return [c for c in self.chats if user_id in c.usersId]

    def get_notifications_by_user(self, user_id: int) -> List[Notification]:
        return [n for n in self.notifications if n.userId == user_id]

    def get_market_items_by_user(self, user_id: int) -> List[MarketplaceItem]:
        return [i for i in self.marketplaceItems if i.sellerId == user_id]

    def get_achievements_by_user(self, user_id: int) -> List[Achievement]:
        return [a for a in self.achievements if a.userId == user_id]


if __name__ == "__main__":
    # parser = Parser()
    # parser.parser_xml("lab1/data/data.xml")

    # # Пример вывода
    # for user in parser.users:
    #     posts = parser.get_posts_by_user(user.userId)
    #     print(f"👤 {user.get_full_name()} — постов: {len(posts)}, ")
    
    # w = parser.get_achievements_by_user(101001)
    # for ach in w:
    #     print(ach.title)
        
    parser = Parser()
    parser.parser_json("lab1/data/data.json")

    # Пример вывода
    for user in parser.users:
        posts = parser.get_posts_by_user(user.userId)
        print(f"👤 {user.get_full_name()} — постов: {len(posts)}, ")
