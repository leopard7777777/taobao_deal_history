#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    @Date:    2016-07-18 15:53:21
    @Author: King
    @Desc:  
"""
import re
from ..items import DealData
from scrapy.loader.processors import TakeFirst, Join
from scrapy import Selector
from scrapy.loader import ItemLoader
import scrapy


class DealItemLoader(ItemLoader):
    default_output_processor = TakeFirst()


class DealHistory(scrapy.Spider):
    name = 'deal_history'

    def __init__(self, seller_id=None, item_id=None, size=100, *args, **kwargs):
        super(DealHistory, self).__init__(*args, **kwargs)
        self.seller_id = seller_id
        self.item_id = item_id
        self.page = 1
        self.size = size

    def start_requests(self):
        return [scrapy.Request("https://licai.taobao.com/json/show_buyer_list.html?bid_page=%s&item_id=%s&seller_id=%s&page_size=%s" % (self.page, self.item_id, self.seller_id, self.size), meta={'dont_obey_robotstxt': True}, callback=self._history)]

    def _history(self, response):
        content = re.findall('\$callback\({html:"(.*?)"}\)', response.body)
        if content:
            sel = Selector(text=content[0].replace(r'\"', '"').replace(r"\'", "'").decode('gbk'))
            trs = sel.xpath('//div[@class="fnc-item-buyerlist"]/table//tr')
            if len(trs) < 2:
                return
            else:
                for tr in trs[1:]:
                    deal = DealItemLoader(DealData(), tr)
                    deal.add_xpath('buyer', './/td[@class="fnc-item-tb-buyer"]/text()', TakeFirst())
                    deal.add_xpath('title', './/td[@class="fnc-item-tb-name"]/span/text()', Join())
                    deal.add_xpath('price', './/td[@class="fnc-item-tb-price"]/text()', TakeFirst())
                    deal.add_xpath('date', './/td[@class="fnc-item-tb-date"]/text()', TakeFirst())
                    deal.add_xpath('status', './/td[@class="fnc-item-tb-status"]/text()', TakeFirst())
                    yield deal.load_item()
                self.page += 1
                yield scrapy.Request("https://licai.taobao.com/json/show_buyer_list.html?bid_page=%s&item_id=%s&seller_id=%s&page_size=%s" % (self.page, self.item_id, self.seller_id, self.size), meta={'dont_obey_robotstxt': True}, callback=self._history)
