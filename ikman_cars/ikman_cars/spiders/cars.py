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
        if 'https://ikman.lk/en/ads/sri-lanka/cars-vehicles?categoryType=ads&categoryName=Cars+%26+Vehicles&page=' in response.url:
            # listing page
            links = response.xpath(
                '//div[@class="serp-items"]/div[contains(@class, "ui-item")]/div[@class="item-content"]/a/@href').extract()
            for link in links:
                yield scrapy.Request('https://ikman.lk/' + link, callback=self.parse)
        else:
            # car advertisements
            title = response.xpath('//div[@class="item-top col-12 lg-8"]/h1/text()').extract_first()
            brand = response.xpath('//div[@class="item-properties"]/dl[1]/dd/text()').extract_first()
            model_year = response.xpath('//div[@class="item-properties"]/dl[2]/dd/text()').extract_first()
            condition = response.xpath('//div[@class="item-properties"]/dl[3]/dd/text()').extract_first()
            transmission = response.xpath('//div[@class="item-properties"]/dl[4]/dd/text()').extract_first()
            model = response.xpath('//div[@class="item-properties"]/dl[5]/dd/text()').extract_first()
            body_type = response.xpath('//div[@class="item-properties"]/dl[6]/dd/text()').extract()
            fuel_type = response.xpath('//div[@class="item-properties"]/dl[7]/dd/text()').extract()
            engine_capacity = response.xpath('//div[@class="item-properties"]/dl[8]/dd/text()').extract()
            mileage = response.xpath('//div[@class="item-properties"]/dl[9]/dd/text()').extract_first()
            yield {
                'title': title,
                'brand': brand,
                'model_year': model_year,
                'condition': condition,
                'transmission': transmission,
                'model': model,
                'body_type': body_type,
                'fuel_type': fuel_type,
                'engine_capacity': engine_capacity,
                'mileage': mileage
            }
