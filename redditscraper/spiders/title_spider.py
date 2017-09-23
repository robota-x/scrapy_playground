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


class CommentSpider(scrapy.Spider):
    name = 'comments'

    def start_requests(self):
        yield scrapy.Request(
            url='https://reddit.com',
            callback=self.parse_top_level
        )

    def parse_top_level(self, response):
        selector_string = '//ul[contains(@class, "flat-list")]/li/a/@href'
        comment_link_list = response.xpath(selector_string).extract()

        for comment_link in comment_link_list:
            yield response.follow(
                url=comment_link,
                callback=self.parse_comments
            )

    def parse_comments(self, response):
        pass
