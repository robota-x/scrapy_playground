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
        link_selector = '//ul[contains(@class, "flat-list")]/li/a/@href'
        comment_link_list = response.xpath(link_selector).extract()

        for comment_link in comment_link_list:
            yield response.follow(
                url=comment_link,
                callback=self.parse_comments
            )

    def parse_comments(self, response):
        comment_selector = '//div[@class="commentarea"]//div[contains(@class, "usertext-body")]/div[@class="md"]'
        comment_list = response.xpath(comment_selector)

        for comment_text in comment_list:
            yield {
                # extract all elements as a list
                'text': comment_text.xpath('*').extract()
            }
