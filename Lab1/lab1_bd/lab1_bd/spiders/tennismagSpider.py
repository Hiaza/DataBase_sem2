import scrapy


class TennismagSpider(scrapy.Spider):
    name = "tennismag"
    fields = {
        'link_pagination': '//div[@class="navigation-pages"]//a/@href',
        'product': '//div[@class="bxr-element-container"]',
        'price': './/span[@class="bxr-market-current-price bxr-market-format-price"]/text()',
        'old_price': './/span[@class="bxr-market-old-price"]/text()',
        'name': './/div[@class="bxr-element-name"]/a/@title',
        'img': './div[@class="bxr-element-image"]/a/img/@src',
        'product_link': './div[@class="bxr-element-image"]/a/@href'
    }
    custom_settings = {
        'CLOSESPIDER_PAGECOUNT': 0,
        'CLOSESPIDER_ITEMCOUNT': 20
    }
    start_urls = [
        'https://tennismag.com.ua/catalog/raketki'
    ]
    allowed_domains = [
        'tennismag.com.ua'
    ]

    def parse(self, response):

       for product in response.xpath(self.fields["product"]):
            price = product.xpath(self.fields['price']).get()
            yield {
                'link': "https://tennismag.com.ua" + product.xpath(self.fields['product_link']).extract()[0],
                'price': price.strip() if price else product.xpath(self.fields['old_price']).get().strip(),
                'img': "https://tennismag.com.ua" + product.xpath(self.fields['img']).extract()[0],
                'name': product.xpath(self.fields['name']).extract()
            }
