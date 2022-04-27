import scrapy

class ForumContent(scrapy.Item):
    username = scrapy.Field()
    posts_quantity = scrapy.Field()
    date_joined = scrapy.Field()
    reputation = scrapy.Field()
    info_date_post = scrapy.Field()
    post_content = scrapy.Field()