import uuid
from datetime import date
from typing import List
from dataclasses import dataclass

@dataclass
class Selenium_Scrapy_Cognos_Dataclass_Breached:
    uuid: uuid.uuid4() 
    username: str
    posts_quantity: int
    date_joined: date
    reputation: int
    info_date_post: str
    post_content: List[str]
    is_admin: bool # For future use
    is_special_user: bool # For future use
    title: str
    post_interatcion: str
    url: str