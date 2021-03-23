import scrapy

from .utils import coin_telegraph_start_urls


class CoinTelegraphSpider(scrapy.Spider):
    name = 'CoinTelegraphSpider'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_urls = coin_telegraph_start_urls()

    def parse(self, response, **kwargs):
        try:
            pub_date = response.css('.post-meta__publish-date').xpath('time').attrib['datetime']
        except KeyError:
            pub_date = 'NONE'

        try:
            news_type = response.css('.post-cover__badge::text').get()
        except IndexError:
            news_type = 'NONE'

        try:
            shares = int(response.css('.post-actions__item-count::text').getall()[1])
        except IndexError:
            shares = None

        try:
            views = int(response.css('.post-actions__item-count::text').getall()[0])
        except IndexError:
            views = None

        yield {
            'date': pub_date,
            'type': news_type,
            'views': views,
            'shares': shares,
            'tags': response.css('.tags-list__list *::text').getall(),
            'title': response.css('.post__title::text').get(),
            'description': response.css('.post__lead::text').get(),
            'body': ' '.join(response.css('.post-content *::text').getall()),
            'url': response.url
        }
