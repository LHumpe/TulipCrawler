import scrapy

from .utils import coin_desk_start_urls


class CoinDeskArticleSpider(scrapy.Spider):
    name = "CoinDeskSpider"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_urls = coin_desk_start_urls()

    def parse(self, response, **kwargs):
        try:
            pub_date = response.xpath(
                '/html/body/div/div[2]/main/section/div[1]/div[1]/article/header/div/div/div[2]/div[2]/div/div[1]/time[1]'
            ).attrib[
                'datetime']
        except KeyError:
            pub_date = 'NONE'

        try:
            news_type = response.xpath(
                '/html/body/div/div[2]/main/section/div[1]/div[1]/article/header/div/div/div[1]/div[1]/a/button/span/strong/text()').get()
        except IndexError:
            news_type = 'NONE'

        yield {
            'date': pub_date,
            'type': news_type,
            'tags': response.css('.tags *::text').getall()[1:],
            'title': response.xpath(
                '/html/body/div/div[2]/main/section/div[1]/div/article/header/div/div/div[1]/div[2]/h1/text()'
            ).get(),
            'description': response.xpath(
                '/html/body/div/div[2]/main/section/div[1]/div[1]/article/header/div/div/div[1]/div[3]/p/text()'
            ).get(),
            'body': ' '.join(response.css('.article-pharagraph *::text').getall()),
            'url': response.url
        }
