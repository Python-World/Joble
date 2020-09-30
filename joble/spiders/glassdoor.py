# -*- coding: utf-8 -*-
import scrapy
import urllib

# scrapy crawl Glassdoor
class GlassdoorSpider(scrapy.Spider):
    name = 'Glassdoor'
    allowed_domains = ['glassdoor.com']

    def __init__(self, keyword=None, count=20):
        self.keyword = keyword
        self.count = int(count)

    def start_requests(self):
        url = 'https://www.glassdoor.com/Job/jobs.htm?sc.keyword={}'.format(self.keyword)
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        elements = response.css('ul.jlGrid li.react-job-listing')
        jobs = []
        
        for element in elements[:self.count]:
            job = {
                'title': element.attrib['data-normalize-job-title'],
                'location': element.attrib['data-job-loc'],
                'employer': 'https://www.glassdoor.com' + element.css('div div.jobHeader a span::text').get(),
                'job-link': element.css('div div.jobHeader a::attr(href)').get()
            }
            jobs.append(job)
        
        print(jobs)