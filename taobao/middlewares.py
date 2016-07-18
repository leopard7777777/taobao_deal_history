#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    @Date:    2016-07-18 15:58:25
    @Author: King
    @Desc:  
"""

import random
import logging

_logger = logging.getLogger(__name__)


class DownloaderMiddleware():
    def process_request(self, request, spider):
        ios = "%s.%s" % (random.randint(30, 50), random.randint(10, 99))
        chrome = random.randint(30, 50)
        OS = random.choice(('Windows NT 6.1; WOW64', 'X11; Linux x86_64', 'Windows NT 5.1', 'Windows NT 6.0',
                            'Windows NT 6.2; WOW64', 'Windows NT 6.2', 'Macintosh; Intel Mac OS X 10_8_0'))
        agent = "Mozilla/5.0 (%s) AppleWebKit/5%s (KHTML, like Gecko) Chrome/%s.0.2623.110 Safari/5%s" % (OS, ios, chrome, ios)
        request.headers['User-Agent'] = agent
        # _logger.info(request.headers)
        pass
