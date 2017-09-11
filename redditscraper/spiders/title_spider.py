import scrapy


class TitleSpider(scrapy.Spider):
    name = 'titles'

    def start_requests(self):
        yield scrapy.Request(
            url='https://reddit.com',
            callback=self.parse
        )

    def parse(self, response):
        file_name = 'results/title_list.html'

        with open(file_name, 'wb') as file:
            file.write(response.body)
        self.log('saved {file_name}'.format(file_name=file_name))
