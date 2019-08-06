import logging

import scrapy
from scrapy.utils.log import configure_logging


class ArticleItem(scrapy.Item):
    configure_logging(install_root_handler=False)
    logging.basicConfig(filename='log.txt', format='%(levelname)s: %(message)s', level=logging.INFO)
    article_url = scrapy.Field()
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
