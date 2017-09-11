import scrapy


class TitleSpider(scrapy.Spider):
    name = 'titles'

    def start_requests(self):
        yield scrapy.Request(
            url='https://reddit.com',
            callback=self.parse
        )

    def parse(self, response):
        title_list = response.xpath('//p[@class="title"]')

        for title in title_list:
            yield {
                'text': title.xpath('.//a/text()').extract_first(),
                'url': title.xpath('.//a/@href').extract_first()
            }
