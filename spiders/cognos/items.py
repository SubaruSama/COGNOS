# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field
from scrapy.loader import ItemLoader
from itemloaders.processors import MapCompose
from w3lib.html import remove_comments, remove_entities, remove_tags


class CognosItem(Item):
    username = Field(input_processor=MapCompose(remove_tags))
    posts_quantity = Field(input_processor=MapCompose(remove_tags))
    date_joined = Field(input_processor=MapCompose(remove_tags))
    reputation = Field(input_processor=MapCompose(remove_tags))
    info_date_post = Field(input_processor=MapCompose(remove_tags))
    post_content = Field(input_processor=MapCompose(remove_tags))
    # is_admin = Field() Uso futuro. Muito provavel terei que remodelar
    # is_special_user = Field() Uso futuro. Muito provavel terei que remodelar
    title = Field(input_processor=MapCompose(remove_tags))
