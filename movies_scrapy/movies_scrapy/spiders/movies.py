import scrapy


class MoviesSpider(scrapy.Spider):
    name = "movies"

    custom_settings = {"DOWNLOAD_DELAY": 2,
                       "CONCURRENT_REQUESTS_PER_DOMAIN": 2}

    def start_requests(self):
        start_url = 'http://www.imdb.com/list/ls057823854/'
        yield scrapy.Request(url=start_url, callback=self.get_movies)

    def get_movies(self, response):
        url_base = 'http://www.imdb.com'
        for i in response.xpath('//div[contains(@class, "list_item")]'):
            url_path = i.xpath('./div[@class="info"]/b/a/@href').extract()[0]
            url = url_base + url_path
            yield scrapy.Request(url=url, callback=self.parse)
        try:
            next_page = response.xpath('//div[@class="pagination"]/a[contains(text(),"Next")]/@href')\
                                .extract()[0]
            list_url = 'http://www.imdb.com/list/ls057823854/'
            next_url = list_url + next_page
            yield scrapy.Request(url=next_url, callback=self.get_movies)
        except:
            next

    def parse(self, response):
        try:
            yield {'title': response.xpath('//title/text()').extract(),
                   'rating': response.xpath('//div[@class="subtext"]/text()').extract()[1],
                   'runtime': response.xpath('//time[@itemprop="duration"]/text()').extract(),
                   'budget': response.xpath('//div[@class="article"]/div[7]/text()').extract(),
                   'genre': response.xpath('//div[@id="titleStoryLine"]/div[4]/a/text()').extract(),
                   'release': response.xpath('//div[@id="titleDetails"]/div[4]/text()').extract(),
                   'imdb_rating': response.xpath('//span[@itemprop="ratingValue"]/text()').extract(),
                   'director': response.xpath('//span[@itemprop="director"]/a/span/text()').extract(),
                   'writer': response.xpath('//span[@itemprop="creator"]/a/span/text()').extract_first(),
                   'actors': response.xpath('//span[@itemprop="actors"]/a/span/text()').extract(),
                   'meta_score': response.xpath('//div[@class="titleReviewBarItem"]/a/div/span/text()').extract(),
                   'opening_weekend': response.xpath('//div[@class="article"]/div[8]/text()').extract()}
        except:
            next
