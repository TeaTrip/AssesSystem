import scrapy
import validators

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from imgscrape.items import ImgscrapeItem


class ImgSpider(CrawlSpider):
    name = 'img'

    def __init__(self, category='', **kwargs):
        self.start_urls = [f'https://www.google.com/search?q={category}&sxsrf=ALiCzsaiRLvxUO0O7q_fr57KJgB6sAfLNw:1667127131970&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjKi_zD5If7AhWWDRAIHX6nCh4Q_AUoAXoECAEQAw&biw=1920&bih=937&dpr=1']  # py36
        super().__init__(**kwargs)  # python3

    rules = (Rule(LinkExtractor(allow=()), callback='item_callback', process_links='link_callback', follow=False),)

    def link_callback(self, links):
        return links

    def item_callback(self, response):
        item = ImgscrapeItem()
        urls = response.css('img').xpath('@src').extract()
        item['image_urls'] = [url for url in urls if validators.url(url)]
        return item
