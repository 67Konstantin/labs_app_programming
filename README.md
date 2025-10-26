## Итоговые пользовательские классы
<details>
<summary><h2>User</h2></summary>

### **Поля**

>userId : int  
firstName : str  
lastName : str  
description : str  
avatarUrl : str  
email : str  
lastActive : datetime  
achievements : List[Achievement]  
followers : Set[int]  
following : Set[int]  
_posts : List[Post]

### **Методы**

>__init__(...)  
get_full_name() -> str  
follow(userId : int) -> None  
unfollow(userId : int) -> None  
add_post(post : Post) -> None  
get_followers(users : list) -> List[User]  
get_following(users : list) -> List[User]
</details>

---

<details>
<summary><h2>Post</h2></summary>

### **Поля**

>postId : int  
userId : int  
text : str  
mediaUrls : List[str]  
likesCount : int  
repostsCount : int  
comments : List[int]  
likedBy : List[int]  
timePublish : datetime  
isDeleted : bool

### **Методы**

>__init__(...)  
add_like(userId : int) -> None  
remove_like(userId : int) -> None  
add_comment(commentId : int) -> None  
delete() -> None
</details>

---

<details>
<summary><h2>Comment</h2></summary>

### **Поля**

>commentId : int  
userId : int  
text : str  
mediaUrls : List[str]  
likesCount : int  
answerTo : int  
timePublish : datetime  
isDeleted : bool  
likedBy : List[int]  
replies : List["Comment"]

### **Методы**

>__init__(...)  
add_reply(reply : "Comment") -> None  
like(userId : int) -> None  
unlike(userId : int) -> None  
delete() -> None
</details>

---

<details>
<summary><h2>Notification</h2></summary>

### **Поля**

>notificationId : int  
userId : int  
timePublish : datetime  
text : str  
clickUrl : str  
isRead : bool  
isOpened : bool

### **Методы**

>__init__(...)  
markAsRead() -> None  
open() -> None
</details>

---

<details>
<summary><h2>Chat</h2></summary>

### **Поля**

>chatId : int  
usersId : List[int]  
createdAt : datetime  
avatarUrl : str  
title : str  
_messages : List[Message]  
_messageCounter : int

### **Методы**

>__init__(...)  
add_user(userId : int) -> None  
remove_user(userId : int) -> None  
send_message(userId : int, text : str, mediaUrls : Optional[List[str]]) -> Message  
get_messages() -> List[Message]
</details>

---

<details>
<summary><h2>Message</h2></summary>

### **Поля**

>messageId : int  
chatId : int  
userId : int  
text : str  
mediaUrls : List[str]  
timeSent : datetime  
isRead : bool  
isEdited : bool  
isDeleted : bool

### **Методы**

>__init__(...)  
mark_as_read() -> None  
edit(newText : str) -> None  
delete() -> None
</details>

---

<details>
<summary><h2>Story</h2></summary>

### **Поля**

>storyId : int  
userId : int  
description : str  
mediaUrl : str  
viewersCount : int  
reactions : List[Reaction]  
_viewers : Set[int]  
timePublish : datetime  
_isArchived : bool  
_isDeleted : bool

### **Методы**

>__init__(...)  
view(userId : int) -> None  
getViewers(users : list) -> List[User]  
archive() -> None  
delete() -> None  
getReactions() -> List[Reaction]  
addReaction(reaction : Reaction) -> None
</details>

---

<details>
<summary><h2>Achievement</h2></summary>

### **Поля**

>achievementId : int  
title : str  
description : str  
iconUrl : str  
isUnlocked : bool  
unlockedAt : Optional[datetime]  
userId : Optional[int]

### **Методы**

>__init__(...)  
unlock(userId : int) -> None  
is_achieved() -> bool  
assign_to_user(userId : int) -> None
</details>

---

<details>
<summary><h2>MarketplaceItem</h2></summary>

### **Поля**

>itemId : int  
title : str  
description : str  
photoUrls : List[str]  
sellerId : int  
price : float  
status : str  
createdAt : datetime

### **Методы**

>__init__(...)  
mark_as_sold() -> None  
update_price(newPrice : float) -> None  
deactivate() -> None
</details>

---

<details>
<summary><h2>Reaction</h2></summary>

### **Поля**

>reactionId : int  
userId : int  
type : str  
createdAt : datetime  
isRemoved : bool

### **Методы**

>__init__(...)  
changeType(newType : str) -> None  
get_user(users : list) -> User
</details>

---

# Ход работы
Первым делом продумываем каждый из 10 классов, поля и методы класса
Затем заходим в figma и для простоты и удобства создаём отдельный компонент, куда будем помещать необходимые данные и создаем диаграммы классов
Создаем github репозиторий и загружаем туда диаграммы
Реализуем классы в отдельных файлах, примерно продумывая реализацию методов
Создаём файл с экспортом и используем всё из этого файла каждый раз когда хотим обратиться к классу
<p>
  <img width="20%" alt="image1" src="https://github.com/user-attachments/assets/5db95be2-3d17-4ed1-87e7-36263c39de49" />
  <img width="75%" alt="image" src="https://github.com/user-attachments/assets/63f9145b-bd4f-4082-ad28-7470bdea8f3d" />
</p>
Создаем файл .gitignore и добавляем туда генерируемые файлы как из папки __pycache__

Коммитим файлы и периодически пушим на протяжении всего проекта

По поводу самих файлов, то при импорте пишем from exports import *
На примере User можно сказать, что поля класса записываем в __init__ 

```python
def __init__(self, userId: int, firstName: str, lastName: str,
                 description: str, avatarUrl: str, email: str):
        self.userId = userId
        self.firstName = firstName
        self.lastName = lastName
        self.description = description
        self.avatarUrl = avatarUrl
        self.email = email
        self.lastActive = datetime.now()
        self.achievements: list[Achievement] = []

        self._followers: set["User"] = set()
        self._following: set["User"] = set()
```

Далее создаем методы. Например getFullName, который возвращает str и пишем это в соответствующем месте для автоматической аннотации в файлах

```python
def getFullName(self) -> str:
        return f"{self.firstName} {self.lastName}"
```

Точно также используем и другие функции и пишем соответствующие None

```python
def addAchievement(self, achievement: Achievement) -> None:
        self.achievements.append(achievement)
```

Таким образом создаем все 10 классов по диаграммам

Создаем примерные данные в файле data/data.json

Затем пишем тоже самое в xml файле в соответствующем формате

А после реализуем парсер в файле parser.py, который в качестве параметров принимает str path

Для этого создаем класс Parser, в котором в функции __init__ читаем файл и сопоставляем данные

На примере User можем разобраться

```python
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
```

Тут создается массив юзеров, где в качестве u мы перебираем каждого json-юзера и сопоставляем с полями в классе. Если в некоторых полях null, то ставим свои значения

Так делаем со всеми объектами всех классов и для проверки в консоль пишем сколько и чего создано

Создадим для проверки несколько методов в Parser, которые после вызовем в самом файле, передав путь до файла json

После всего этого, правок в процессе получаем такие классы и архитектуру

<p>
  <img width="13%" alt="image" src="https://github.com/user-attachments/assets/b308e598-30ed-47e3-b2e7-cfea2d7c3061" />
  <img width="84%" alt="image" src="https://github.com/user-attachments/assets/54c4d80e-49c7-48dd-8139-90218bc01191" />
</p>

После этого стоит сделать обработку исключений. На примере User разберем как это делается

```python
if not isinstance(userId, int) or not str(userId).startswith("101"):
            raise TypeError("userId должен быть int и начинаться с 101.")
        self.userId = userId

        if not isinstance(firstName, str) and firstName.strip():
            raise ValueError("firstName должен быть непустой строкой.")
        self.firstName = firstName

        if not isinstance(lastName, str) and lastName.strip():
            raise ValueError("lastName должен быть непустой строкой.")
        self.lastName = lastName

        if not isinstance(description, str):
            raise ValueError("description должен быть строкой.")
        self.description = description

        if not isinstance(avatarUrl, str) or not (avatarUrl.startswith("http://") or avatarUrl.startswith("https://")):
            raise ValueError("Некорректный формат avatarUrl (должен начинаться с http:// или https://).")
        self.avatarUrl = avatarUrl

        if not isinstance(email, str) or '@' not in email or '.' not in email.split('@')[-1]:
            raise ValueError("Некорректный формат email.")
        self.email = email

        if not isinstance(lastActive, datetime):
            raise TypeError("lastActive должен быть экземпляром datetime.")
        self.lastActive = lastActive

        if achievements is not None:
            if not isinstance(achievements, list):
                raise TypeError("achievements должен быть списком (list) или None.")
            for ach in achievements:
                if not isinstance(ach, Achievement):
                    raise TypeError("Все элементы achievements должны быть экземплярами Achievement.")
        self.achievements = achievements or []


        if followers is not None:
            if not isinstance(followers, set):
                raise TypeError("followers должен быть множеством (set) или None.")
            for f in followers:
                if not isinstance(f, int):
                    raise TypeError("Все элементы followers должны быть экземплярами int.")
        self.followers = followers or set()


        if following is not None:
            if not isinstance(following, set):
                raise TypeError("following должен быть множеством (set) или None.")
            for u in following:
                if not isinstance(u, int):
                    raise TypeError("Все элементы following должны быть экземплярами int.")
        self.following = following or set()
```

Тут можно заметить обработку исключений формата сравнения типа данных и другой валидации, например для почты, ссылок или userid