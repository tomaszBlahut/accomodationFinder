import scrapy


class BiedronkaSpider(scrapy.Spider):
    name = "biedronka"
    shops_with_404 = 0

    def start_requests(self):
        url = 'http://www.biedronka.pl/index.php/pl/shop,id,2878'
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        if response.status == 200:
            self.shops_with_404 = 0
            yield {
                'id': response.url.split(",")[-1],

                'city':
                response.css(".shopName::text").extract_first(),

                'street':
                ' '.join(response.css(".shopFullAddress ::text").extract()),

                'latitude':
                response.css(".shopMapContainer::attr(data-latitude)")
                .extract_first(),

                'longitude':
                response.css(".shopMapContainer::attr(data-longitude)")
                .extract_first()
            }
        else:
            self.shops_with_404 += 1

        if self.shops_with_404 < 100:
            current_shop_id = response.url.split(",")[-1]
            yield response.follow(response.url.replace(
                current_shop_id, str(int(current_shop_id)+1)),
                callback=self.parse)
