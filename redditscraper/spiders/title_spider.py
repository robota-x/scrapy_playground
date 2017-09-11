import scrapy


class TitleSpider(scrapy.Spider):
    name = 'titles'

    def start_requests(self):
        yield scrapy.Request(
            url='https://reddit.com',
            callback=self.parse
        )

    def parse(self, response):
        title_list = response.xpath('//p[@class="title"]/a/text()').extract()
        file_name = 'results/title_list.txt'
        with open(file_name, 'wb') as file:
            for title in title_list:
                file.write(title + '\n')
        self.log('saved {file_name}'.format(file_name=file_name))
