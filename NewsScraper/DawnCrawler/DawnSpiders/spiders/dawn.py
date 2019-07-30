# -*- coding: utf-8 -*-
import scrapy
from scrapy import Item
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class DawnscraperItem(Item):
    title = scrapy.Field()
    image_urls = scrapy.Field()
    published_date = scrapy.Field()
    updated_date = scrapy.Field()
    authors = scrapy.Field()
    tweets = scrapy.Field()
    comments = scrapy.Field()
    content = scrapy.Field()
    category = scrapy.Field()


class DawnSpider(CrawlSpider):
    name = 'dawn'
    allowed_domains = ['dawn.com']
    start_urls = [
        "https://www.dawn.com/latest-news",
        "https://www.dawn.com/business",
        "https://www.dawn.com/opinion",
        "https://www.dawn.com/prism",
        "https://www.dawn.com/sport",
        "https://www.dawn.com/magazines",
        "https://www.dawn.com/world",
        "https://www.dawn.com/tech",
        "https://www.dawn.com/multimedia",
        "https://www.dawn.com/in-depth/"
    ]

    rules = (
        Rule(
            LinkExtractor(allow='.*/news/.*'),
            callback='parse_items', follow=True),

    )

    def parse_items(self, response):

        article = DawnscraperItem()
        article['title'] = response.css("a.story__link::text")[0].extract().replace("\n", " ")

        image_urls = [response.css('.media__item img').xpath('@src').get(),
                      response.css(".story__content .media--expand-25 img::attr(src)").extract(),
                      response.xpath('/html/body/div/div/figure/div/img').xpath('@src').extract()]

        image_urls = [image_index for image_index in image_urls if image_index != []]
        article['image_urls'] = image_urls

        published_date = response.css("span.story__time::text")[0].extract()
        article['published_date'] = published_date

        article['updated_date'] = response.css(".timestamp--time::text").extract()

        if "|" in response.css(".text-grey a::text")[0].extract():
            article['authors'] = response.css(".sm-inline-block.sm-float-left a::text").extract()
        else:
            article['authors'] = response.css(".text-grey a::text").extract()

        article['tweets'] = response.css(".Twitter-tweet a::attr(href)").extract()

        article['comments'] = response.css(".comment__body p::text").extract()

        content = response.css(".pt-4 p::text").extract()
        content.append(response.css(".mt-1 p::text").extract())
        content.append(response.css(".story__content p::text").extract())

        content = [content_index for content_index in content if content_index != []]

        content = ' '.join(map(str, content[0]))
        article['content'] = content.replace("\n", " ")

        article['category'] = response.css(".active a::text").get()

        return article
