import uuid
from datetime import date
from typing import List
from dataclasses import dataclass

@dataclass
class Selenium_Cognos_Dataclass_Breached:
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

	def __str__(self) -> str:
		return(
			"uuid: {self.uuid}",
			"username: {self.username}",
			"posts_quantity: {self.posts_quantity}",
			"date_joined: {self.date_joined}",
			"reputation: {self.reputation}",
			"info_date_post: {self.info_date_post}",
			"post_content: {self.post_content}",
			"title: {self.title}",
			"post_interaction: {self.post_interaction}",
			"url: {self.url}"
		)

	
