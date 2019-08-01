from DawnSpiders.items import ArticleItem
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class DawnSpider(CrawlSpider):
    name = 'dawn'
    allowed_domains = ['dawn.com']
    start_urls = [
        "https://www.dawn.com/"

    ]
    rules = (
        Rule(
            LinkExtractor(restrict_css= "[class^='nav__item nav__item--']"),
            callback='parse',
            follow=True
        ),
        Rule(
            LinkExtractor(restrict_css='.story'),
            callback='parse_items',
            follow=True
        ),

    )

    def parse_items(self, response):
        article = ArticleItem()
        if response.xpath("//*[@itemprop='name']/@content").get():
            article['title'] = response.xpath("//*[@itemprop='name']/@content").get().replace("\n", " ")
        else:
            article['title'] = "Not given"
        article['cover_image_url'] = response.css(".media--uneven img::attr(src)").get()
        article['image_urls'] = response.css(".media--center ::attr(src)").getall()
        article['published_time'] = response.xpath("//*[@property='article:published_time']/@content").get()
        article['updated_time'] = response.css(".timestamp--time::text").getall()
        article['authors'] = response.xpath("//*[@name='author']/@content").get()
        article['tweets'] = response.css(".Twitter-tweet a::attr(href)").getall()
        user = response.css(".comment__author::text").getall()
        comment = response.css(".comment__body p::text").getall()
        # below logic converts users and comments into a list of dictionaries
        article['comments'] = [{'user': user[comm_indx], 'content': comment[comm_indx]} for comm_indx in
                               range(len(user))]
        # content is returned as a list, so below logic joins it into a string
        article['content'] = response.css(".story__content ::text").getall()
        article['content'] = ' '.join(article['content'])
        article['content'] = article['content'].replace("\n", " ").replace("\t", " ")
        article['category'] = response.css(".active a::text").get()
        return article
