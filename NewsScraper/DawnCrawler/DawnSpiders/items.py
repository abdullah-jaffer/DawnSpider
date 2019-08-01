import scrapy


class ArticleItem(scrapy.Item):

    title = scrapy.Field()
    image_urls = scrapy.Field()
    published_time = scrapy.Field()
    updated_time = scrapy.Field()
    authors = scrapy.Field()
    tweets = scrapy.Field()
    comments = scrapy.Field()
    content = scrapy.Field()
    category = scrapy.Field()
    cover_image_url = scrapy.Field()

