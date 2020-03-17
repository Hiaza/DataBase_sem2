import scrapy


def isNotEmptyString(str):
    return len(str) > 0


class ShkolaSpider(scrapy.Spider):
    name = "shkolaua"
    custom_settings = {
        'ITEM_PIPELINES': {
            'lab1_bd.pipelines.Lab1BdPipeline': 300,
        }
    }
    fields = {
        'img': '//img/@src',
        'text': '//*[not(self::script)]/text()',
        'link': '//a/@href'
    }
    start_urls = [
        'http://shkola.in.ua',
        'http://shkola.in.ua/pidruchnyky/Page-2.html'
    ]
    allowed_domains = [
        'shkola.in.ua'
    ]

    def parse(self, response):
        text = filter(isNotEmptyString,
                      map(lambda str: str.strip(),
                          [text.extract() for text in response.xpath(self.fields["text"])]))
        images = map(lambda url: ((response.url + url) if url.startswith('/') else url),
                     [img_url.extract() for img_url in response.xpath(self.fields["img"])])
        yield {
            'text': text,
            'images': images,
            'url': response.url
        }
        for link_url in response.xpath(self.fields['link']):
            yield response.follow(link_url.extract(), callback=self.parse)
