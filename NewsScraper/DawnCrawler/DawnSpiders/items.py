import scrapy


class ArticleItem(scrapy.Item):

    title = scrapy.Field()
    image_urls = scrapy.Field()
    published_date = scrapy.Field()
    updated_date = scrapy.Field()
    authors = scrapy.Field()
    tweets = scrapy.Field()
    comments = scrapy.Field()
    content = scrapy.Field()
    category = scrapy.Field()
    cover_image_url = scrapy.Field()

