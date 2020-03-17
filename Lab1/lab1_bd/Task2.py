from scrapy import cmdline
import os
import lxml.etree as ET


def crawl():
    try:
        os.remove("results/tennismag.xml")
    except OSError:
        print("results/tennismag.xml not found")
    cmdline.execute("scrapy crawl tennismag -o results/tennismag.xml -t xml".split())


def xslt_parse():
    dom = ET.parse('results/tennismag.xml')
    xslt = ET.parse('tennismag.xslt')
    transform = ET.XSLT(xslt)
    newdom = transform(dom)
    with open('results/tennismag.html', 'wb') as f:
        f.write(ET.tostring(newdom, pretty_print=True))

xslt_parse()
