from scrapy import Item, Field

class ForumContent(Item):
    username = Field()
    posts_quantity = Field()
    date_joined = Field()
    reputation = Field()
    info_date_post = Field()
    post_content = Field()
    is_admin = Field()
    is_special_user = Field()
    title = Field()