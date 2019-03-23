# -*- coding: utf-8 -*-
import scrapy
from collectips.items import CollectipsItem

class XiciSpider(scrapy.Spider):
    name = 'xici'
    allowed_domains = ['xicidaili.com']
    start_urls = ['http://www.xicidaili.com']

    #开始请求地址
    def start_requests(self):
        reqs = []

        for i in range(1,2600):
            req=scrapy.Request("http://www.xicidaili.com/nn/%s"%i)
            reqs.append(req)
        return reqs


    def parse(self, response):

        for info in response.xpath('//table[@id="ip_list"]/tr')[1:]:
            collecte = CollectipsItem()
            collecte['ip'] = info.xpath('td[2]/text()').extract_first()
            collecte['port'] = info.xpath('td[3]/text()').extract_first()
            collecte['address'] = info.xpath('td[4]/a/text()').extract_first()
            collecte['annoy'] = info.xpath('td[5]/text()').extract_first()
            collecte['type'] = info.xpath('td[6]/text()').extract_first()
            collecte['live'] = info.xpath('td[9]/text()').extract_first()
            collecte['check'] =  info.xpath('td[10]/text()').extract_first()

        yield collecte