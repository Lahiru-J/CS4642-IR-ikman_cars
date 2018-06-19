import scrapy


class CarsSpider(scrapy.Spider):
    name = "cars"

    def start_requests(self):
        with open('urls.csv') as f:
            urls = f.readlines()
        urls = [x.strip() for x in urls]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        if 'https://ikman.lk/en/ads/sri-lanka/cars?categoryType=ads&categoryName=Cars&page=' in response.url:
            # listing page
            links = response.xpath('//ul[@class="media-list search-results"]/div[@class="row"]/a/@href').extract()
            for link in links:
                yield scrapy.Request('https://ikman.lk/'+link, callback=self.parse)
        else:
            # restaurant page
            title = response.xpath('//div[@class="item-top col-12 lg-8"]/h1/text()').extract_first()
            brand = response.xpath('//ul[@class="place-title-list list-inline"]/li/a/text()').extract_first()
            model_year = response.xpath('//div[@class="place-title-box"]/p/text()').extract_first()
            transmission = response.xpath('//div[@class="place-title-box"]/p[@class="excerpt"]/text()').extract_first()
            model = response.xpath(
                '//div[@class="author-byline"]/div[@class="media"]/div/div/a/span/text()').extract_first()
            body_type = response.xpath('//p[text()="Cuisine"]/following::p[1]/a/text()').extract()
            fuel_type = response.xpath('//p[text()="Price Range"]/following::p[1]/a/text()').extract()
            engine_capacity = response.xpath('//p[text()="Dish Types"]/following::p[1]/a/text()').extract()
            mileage = response.xpath('//dt/a[text()="Overall Rating"]/following::dd[1]/span/text()').extract_first()
            yield {
                'title': title,
                'brand': brand,
                'model_year': model_year,
                'transmission': transmission,
                'model': model,
                'body_type': body_type,
                'fuel_type': fuel_type,
                'engine_capacity': engine_capacity,
                'mileage': mileage
            }
