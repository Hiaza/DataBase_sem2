from scrapy import cmdline
from lxml import etree

#cmdline.execute("scrapy crawl shkolaua".split())
root = None
with open('results/shkolaua.xml', 'r') as file:
    root = etree.parse(file)

for page in root.xpath('//page'):
    textFragmentsCount = page.xpath('count(fragment[@type="text"])')
    print('Count of text fragments at page - ' + page.xpath('@url')[0])
    print(" " + str(textFragmentsCount) + "\n")
