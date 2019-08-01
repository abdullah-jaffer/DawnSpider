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
            LinkExtractor(restrict_xpaths=[
                "//li[@class='nav__item--pakistan']",
                "//li[@class='nav__item--business']",
                "//li[@class='nav__item--opinion']",
                "//li[@class='nav__item--prism ']",
                "//li[@class='nav__item--entertainment']",
                "//li[@class='nav__item--sport']",
                "//li[@class='nav__item--magazines']",
                "//li[@class='nav__item--world']",
                "//li[@class='nav__item--tech']",
                "//li[@class='nav__item--popular ']",
                "//li[@class='nav__item--multimedia']",
                "//li[@class='nav__item--newspaper']",
                "//li[@class='nav__item--in-depth ']",
            ],

            ),
            callback='parse',
            follow=True
        ),
        Rule(
            LinkExtractor(allow='.*/news/.*'),
            callback='parse_items', follow=True),

    )

    def parse_items(self, response):

        article = ArticleItem()
        article['title'] = response.xpath("//*[@itemprop='name']/@content").get().replace("\n", " ")
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
        article['content'] = ' '.join(map(str, article['content']))
        article['content'] = article['content'].replace("\n", " ").replace("\t", " ")
        article['category'] = response.css(".active a::text").get()
        return article
