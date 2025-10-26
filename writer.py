import json
from datetime import datetime
from typing import List, Optional
from classes import *
from parser import Parser
import xml.etree.ElementTree as ET


class Writer:
    def __init__(self, parser: Parser):
        self.parser = parser

    def to_json(self, path: str = "lab1/data/written_data.json") -> None:
        def serialize(obj):
            if isinstance(obj, datetime):
                return obj.isoformat()
            if isinstance(obj, set):
                return list(obj)
            if hasattr(obj, "__dict__"):
                return obj.__dict__
            return str(obj)

        data = {
            "users": self.parser.users,
            "achievements": self.parser.achievements,
            "posts": self.parser.posts,
            "comments": self.parser.comments,
            "reactions": self.parser.reactions,
            "messages": self.parser.messages,
            "chats": self.parser.chats,
            "stories": self.parser.stories,
            "notifications": self.parser.notifications,
            "marketplaceItems": self.parser.marketplaceItems,
        }
        

        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4, default=serialize)

        print(f"Данные успешно записаны в {path}")
        
    def to_xml(self, path: str = "lab1/data/written_data.xml") -> None:
        # Сохраняет данные с правильной структурой массивов
        def serialize_value(value):
            if isinstance(value, datetime):
                return value.isoformat()
            if isinstance(value, (list, set, tuple)):
                return ", ".join(map(str, value))
            return str(value)

        def build_element(parent, key, value):
            # Добавляет элементы XML
            if isinstance(value, dict):
                elem = ET.SubElement(parent, key)
                for k, v in value.items():
                    build_element(elem, k, v)
            elif isinstance(value, list):
                list_elem = ET.SubElement(parent, key)
                for item in value:
                    item_tag = key[:-1] if key.endswith("s") else "item"
                    build_element(list_elem, item_tag, item)
            elif hasattr(value, "__dict__"):
                obj_elem = ET.SubElement(parent, key)
                for k, v in value.__dict__.items():
                    build_element(obj_elem, k, v)
            else:
                elem = ET.SubElement(parent, key)
                elem.text = serialize_value(value)

        def build_object_element(parent, obj, item_tag):
            # Создает элемент объекта с правильной структурой массивов
            obj_elem = ET.SubElement(parent, item_tag)
            
            for attr_name, attr_value in obj.__dict__.items():
                if attr_name in ['achievements', 'followers', 'following', 'comments', 'likedBy', 
                               'mediaUrls', 'reactions', 'viewers', 'usersId', 'replies', 'photoUrls']:
                    # Это массив, создаем контейнер
                    array_elem = ET.SubElement(obj_elem, attr_name)
                    if isinstance(attr_value, (list, set, tuple)) and attr_value:
                        for item in attr_value:
                            item_elem = ET.SubElement(array_elem, attr_name[:-1] if attr_name.endswith("s") else "item")
                            # Если это объект Reaction, берем его ID
                            if hasattr(item, 'reactionId'):
                                item_elem.text = str(item.reactionId)
                            else:
                                item_elem.text = str(item)
                    elif isinstance(attr_value, str) and attr_value:
                        # Если это строка с разделителями (например, mediaUrls)
                        items = [item.strip() for item in attr_value.split(",") if item.strip()]
                        for item in items:
                            item_elem = ET.SubElement(array_elem, "url" if attr_name == "mediaUrls" or attr_name == "photoUrls" else "item")
                            item_elem.text = item
                else:
                    # Обычное поле
                    elem = ET.SubElement(obj_elem, attr_name)
                    elem.text = serialize_value(attr_value)
            
            return obj_elem

        # Корневой элемент XML
        root = ET.Element("data")

        # Секции данных
        sections = {
            "users": (self.parser.users, "user"),
            "achievements": (self.parser.achievements, "achievement"),
            "posts": (self.parser.posts, "post"),
            "comments": (self.parser.comments, "comment"),
            "reactions": (self.parser.reactions, "reaction"),
            "messages": (self.parser.messages, "message"),
            "chats": (self.parser.chats, "chat"),
            "stories": (self.parser.stories, "story"),
            "notifications": (self.parser.notifications, "notification"),
            "marketplaceItems": (self.parser.marketplaceItems, "marketplaceItem"),
        }

        # Заполняем XML
        for section_name, (items, item_tag) in sections.items():
            section_el = ET.SubElement(root, section_name)
            for item in items:
                build_object_element(section_el, item, item_tag)

        # Создаем и сохраняем XML-файл
        tree = ET.ElementTree(root)
        tree.write(path, encoding="utf-8", xml_declaration=True)

        print(f"Данные успешно записаны в {path}")



if __name__ == "__main__":
    parser = Parser()
    
    print("=========================Парсинг исходного XML======================\n")
    parser.parser_xml("lab1/data/data.xml")
    
    myWriter = Writer(parser)
    
    print("Запись в JSON...")
    myWriter.to_json("lab1/data/written_data.json")
    
    print("Запись в XML...")
    myWriter.to_xml("lab1/data/written_data.xml")
    
    print("\n-----------------------Тестирование парсинга записанных файлов------------------------\n")
    
    parser2 = Parser()
    parser2.parser_json("lab1/data/written_data.json")
    print("с всё JSON норм")
    
    parser3 = Parser()
    parser3.parser_xml("lab1/data/written_data.xml")
    print("с XML всё норм")