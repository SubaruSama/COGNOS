import uuid
from datetime import date
from typing import List, Dict, Optional, Union
from dataclasses import dataclass

@dataclass
class Selenium_Cognos_Dataclass_Breached:
    # uuid: Union[str, uuid.UUID] # For future use
    username: Optional[str] = None
    posts_quantity: Optional[int] = None
    date_joined: Optional[date] = None
    reputation: Optional[int] = None
    info_date_post: Optional[str] = None
    post_content: Optional[List[str]] = None
    # is_admin: Optional[bool] = None # For future use
    # is_special_user: Optional[bool] = None # For future use
    title: Optional[str] = None
    post_interatcion: Optional[str] = None
    url: Optional[str] = None

    def as_dict(self) -> Dict[str, str]:
        return {
            'uuid': self.uuid,
            'username': self.username,
            'posts_quantity': self.posts_quantity,
            'date_joind': self.date_joined,
            'reputation': self.reputation,
            'info_date_post': self.info_date_post,
            'title': self.title,
            'post_content': self.post_content,
            'url': self.url
        }
