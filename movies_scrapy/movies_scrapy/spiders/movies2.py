import scrapy


# new instance of class scrapy.Spider
class MoviesSpider(scrapy.Spider):
    name = "movies2"

    # space out requests to websites
    custom_settings = {"DOWNLOAD_DELAY": 3,
                       "CONCURRENT_REQUESTS_PER_DOMAIN": 3,
                       "HTTPCACHE_ENABLED": True}

    # starting point for spider
    def start_requests(self):
        start_url = 'http://www.imdb.com/list/ls057823854/'
        yield scrapy.Request(url=start_url, callback=self.get_movies)

    # gets additional webpages from imdb master list
    def get_movies(self, response):
        url_list = []
        url_base = 'http://www.imdb.com'
        for i in response.xpath('//div[contains(@class, "list_item")]'):
            url_path = i.xpath('./div[@class="info"]/b/a/@href').extract()[0]
            url = url_base + url_path
            url_list.append(url)
        try:
            next_page = response.xpath('//div[@class="pagination"]/a[contains(text(),"Next")]/@href').extract()[0]
            list_url = 'http://www.imdb.com/list/ls057823854/'
            next_url = list_url + next_page
            yield scrapy.Request(url=next_url, callback=self.get_movies)
        except:
            next
        for item in url_list:
            yield scrapy.Request(url=item, callback=self.parse, meta={'url':item})

    def parse(self, response):
        url = response.request.meta['url']
        url_path = 'business'
        new_url = url + url_path
        try:
            title = response.xpath('//title/text()').extract()
            mpaa_rating = response.xpath('//div[@class="subtext"]/text()').extract()[1]
            runtime_mins = response.xpath('//time[@itemprop="duration"]/text()').extract()
            budget = response.xpath('//div[@id="titleDetails"]/div[7]/text()').extract()
            genre = response.xpath('//div[@id="titleStoryLine"]/div[4]/a/text()').extract()
            release_date = response.xpath('//div[@id="titleDetails"]/div[4]/text()').extract()
            imdb_rating = response.xpath('//span[@itemprop="ratingValue"]/text()').extract()
            director = response.xpath('//span[@itemprop="director"]/a/span/text()').extract()
            writer = response.xpath('//span[@itemprop="creator"]/a/span/text()').extract_first()
            actors = response.xpath('//span[@itemprop="actors"]/a/span/text()').extract()
            meta_score = response.xpath('//div[@class="titleReviewBarItem"]/a/div/span/text()').extract()
            opening_weekend = response.xpath('//div[@id="titleDetails"]/div[8]/text()').extract()
            gross_domestic = response.xpath('//div[@id="titleDetails"]/div[9]/text()').extract()
            dollars = opening_weekend[1]
            if "$" in dollars:
                yield {'title': title,
                       'mpaa_rating': mpaa_rating,
                       'runtime_mins': runtime_mins,
                       'budget': budget,
                       'genre': genre,
                       'release_date': release_date,
                       'imdb_rating': imdb_rating,
                       'director': director,
                       'writer': writer,
                       'actors': actors,
                       'meta_score': meta_score,
                       'opening_weekend': opening_weekend,
                       'gross_domestic': gross_domestic}
            else:
                yield scrapy.Request(url=new_url, callback=self.parse2,
                                     meta={'title': title,
                                           'mpaa_rating': mpaa_rating,
                                           'runtime_mins': runtime_mins,
                                           'budget': budget,
                                           'genre': genre,
                                           'release_date': release_date,
                                           'imdb_rating': imdb_rating,
                                           'director': director,
                                           'writer': writer,
                                           'actors': actors,
                                           'meta_score': meta_score,
                                           'gross_domestic': gross_domestic})
        except:
            next

    def parse2(self, response):
        title = response.request.meta['title']
        mpaa_rating = response.request.meta['mpaa_rating']
        runtime_mins = response.request.meta['runtime_mins']
        budget = response.request.meta['budget']
        genre = response.request.meta['genre']
        release_date = response.request.meta['release_date']
        imdb_rating = response.request.meta['imdb_rating']
        director = response.request.meta['director']
        writer = response.request.meta['writer']
        actors = response.request.meta['actors']
        meta_score = response.request.meta['meta_score']
        gross_domestic = response.request.meta['gross_domestic']
        try:
            opening_weekend = response.xpath('//div[@id="tn15content"]/text()[5]').extract()
            yield {'title': title,
                   'mpaa_rating': mpaa_rating,
                   'runtime_mins': runtime_mins,
                   'budget': budget,
                   'genre': genre,
                   'release_date': release_date,
                   'imdb_rating': imdb_rating,
                   'director': director,
                   'writer': writer,
                   'actors': actors,
                   'meta_score': meta_score,
                   'gross_domestic': gross_domestic,
                   'opening_weekend': opening_weekend}
        except:
            next
