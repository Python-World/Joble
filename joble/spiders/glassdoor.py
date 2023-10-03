# -*- coding: utf-8 -*-
import urllib

import scrapy


# scrapy crawl Glassdoor
class GlassdoorSpider(scrapy.Spider):
    name = "Glassdoor"
    allowed_domains = ["glassdoor.com"]
    url = "https://www.glassdoor.com"

    def __init__(self, keyword=None, count=20):
        self.keyword = keyword
        self.count = int(count)

    def start_requests(self):
        url = "{}/Job/jobs.htm?sc.keyword={}".format(self.url, self.keyword)
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        elements = response.css("ul.jlGrid li.react-job-listing")

        for element in elements[: self.count]:
            job = {
                "title": element.attrib["data-normalize-job-title"],
                "location": element.attrib["data-job-loc"],
                "employer": self.url
                + element.css("div div.jobHeader a span::text").get(),
                "job-link": element.css(
                    "div div.jobHeader a::attr(href)"
                ).get(),
            }
            yield job
