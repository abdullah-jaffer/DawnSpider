# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DawnscraperItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    image_urls = scrapy.Field()
    published_date = scrapy.Field()
    updated_date = scrapy.Field()
    authors = scrapy.Field()
    tweets = scrapy.Field()
    comments = scrapy.Field()
    content = scrapy.Field()
    category = scrapy.Field()
