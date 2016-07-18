#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    @Date:    2016-07-18 15:55:41
    @Author: King
    @Desc:  
"""

from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals

import logging

_logger = logging.getLogger(__name__)

class CrawlServer():

    def __init__(self):
        configure_logging()
        settings = get_project_settings()
        self.runner = CrawlerRunner(settings)

    def runspider(self, spider_id, **spider_args):
        listings = list()

        def _item_passed(item):
            listings.append(item)

        dispatcher.connect(_item_passed, signals.item_passed)

        @defer.inlineCallbacks
        def crawl():
            yield self.runner.crawl(spider_id, **spider_args)
            reactor.stop()

        crawl()
        reactor.run()
        return listings

if __name__ == '__main__':
    server = CrawlServer()
    item_id = '525850484428'
    items = server.runspider('deal_history', item_id=item_id, seller_id='2455547464')
    print items
    # records = pd.DataFrame(items)
    # records.to_excel('%s.xlsx' % item_id)
