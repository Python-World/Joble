# -*- coding: utf-8 -*-
import scrapy
from urllib.parse import urlencode, urljoin
from scrapy import Request

# Execute : scrapy crawl MonsterIndia -a keyword=python
class MonsterindiaSpider(scrapy.Spider):
    name = 'MonsterIndia'
    allowed_domains = ['monsterindia.com']
    start_urls = ['http://monsterindia.com/']

    def __init__(self, keyword, count=20, location=None):
        self.URL = 'http://monsterindia.com/'
        self.count = count
        self.keyword = keyword
        self.location = location

    def get_url(self):
        base_url = 'https://www.monsterindia.com/middleware/jobsearch?'
        params = {
            'sort':	"2",
            'limit': self.count,
            'query': self.keyword,
            'locations': self.location,
        }
        if self.location is None:
            params.pop('locations')
    
        return {'url': base_url,
            'body': urlencode(params)}

    def parse(self, response):
       url = self.get_url()
       yield Request(url['url']+url['body'],
        meta={
            'url': url
        },
        callback=self.JobData)

    def JobData(self, response):
        data = response.text
        data = data.replace('false', 'False')
        data = data.replace('true', 'True')
        jobdata = eval(data)
        if jobdata.get('jobSearchResponse'):
            for record in jobdata['jobSearchResponse']['data']:
                headers = ['jobId', 'title', 'locations', 'updatedAt', 'summary', 'skills', 'companyName', 'seoJdUrl']
                job_details = {}
                for head in headers:
                    try:
                        job_details[head] = record.get(head)
                    except Exception as ex:
                        print('error in head:', head, ex)  
                job_details['seoJdUrl'] = urljoin(self.URL, job_details['seoJdUrl'])
                if job_details['jobId']:
                    yield job_details
