# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose


class DealData(scrapy.Item):

    buyer = scrapy.Field(input_processor=MapCompose(unicode.strip))
    title = scrapy.Field(input_processor=MapCompose(unicode.strip))
    price = scrapy.Field()
    date = scrapy.Field()
    status = scrapy.Field()
