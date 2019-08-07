from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from DawnSpiders.items import ArticleItem


class DawnSpider(CrawlSpider):
    name = 'dawn'
    allowed_domains = ['dawn.com']
    start_urls = [
        "https://www.dawn.com/"

    ]
    custom_settings = {
        'LOG_FILE': 'dawn.log',
    }
    rules = (
        Rule(LinkExtractor(restrict_css="[class^='nav__item nav__item--']", deny=['/authors/', '/print/']),
             process_links='process_links', callback='parse', follow=True),
        Rule(LinkExtractor(restrict_css='.story', deny=['/authors/', '/print/']), process_links='process_links',
             callback='parse_items', follow=True)
    )

    def process_links(self, links):
        for link in links:
            link.url = link.url.rsplit('/', 1)[0]
            yield link

    def parse_items(self, response):
        article = ArticleItem()
        article['article_url'] = response.url
        article['title'] = response.css(".story__link::text").get().replace("\n", " ")
        article['cover_image_url'] = response.css(".media--uneven img::attr(src)").get()
        article['image_urls'] = response.css(".media--center img::attr(src)").getall()
        article['published_time'] = response.xpath("//*[@property='article:published_time']/@content").get()
        article['updated_time'] = response.css(".timestamp--time::text").getall()
        article['authors'] = response.xpath("//*[@name='author']/@content").get()
        article['tweets'] = response.css(".Twitter-tweet a::attr(href)").getall()
        user = response.css(".comment__author::text").getall()
        comment = response.css(".comment__body p::text").getall()
        article['comments'] = [{'user': poster, 'content': content} for poster, content in zip(user, comment)]
        article['content'] = response.css(".story__content ::text").getall()
        article['category'] = response.css(".active a::text").get()

        yield article
