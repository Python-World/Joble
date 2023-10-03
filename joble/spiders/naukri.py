# -*- coding: utf-8 -*-
import urllib

import scrapy


# scrapy crawl Naukri
class NaukriSpider(scrapy.Spider):
    name = "Naukri"
    allowed_domains = ["naukri.com"]
    start_urls = ["https://www.naukri.com"]

    def __init__(self, keyword=None, count=20, city=None):
        self.count = count
        self.keyword = keyword
        self.city = city

    def get_url(self):
        base_url = "https://www.naukri.com/jobapi/v3/search?"
        params = {
            "noOfResults": self.count,
            "urlType": "search_by_key_loc",
            "searchType": "adv",
            "keyword": self.keyword,
            "location": self.city,
            "sort": "r",
            "k": self.keyword,
            "l": self.city,
            "seoKey": "{}-jobs-in-{}".format(self.keyword, self.city)
            if self.city
            else "{}-jobs".format(self.keyword),
            "src": "jobsearchDesk",
            "latLong": "",
        }
        default = ["keyword", "sort", "l", "k", "location"]
        if self.city is None:
            for key in default:
                params.pop(key)
        return {"url": base_url, "body": params}

    def parse(self, response):
        if self.keyword:
            record = self.get_url()
            yield scrapy.Request(
                url=record["url"] + urllib.parse.urlencode(record["body"]),
                headers={
                    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:74.0) Gecko/20100101 Firefox/74.0",
                    "appid": "109",
                    "systemid": "109",
                },
                meta={"keyword": self.keyword},
                callback=self.jobData,
            )
        else:
            yield scrapy.Request(
                "https://www.naukri.com/jobs-by-category",
                callback=self.get_by_category,
            )

    def get_by_category(self, response):
        for j in response.xpath('//div[@class="lmrWrap wrap"]/div/div/div/a'):
            title = j.xpath("text()").get().strip()
            url = j.xpath("@href").get().strip()
            yield scrapy.Request(
                url,
                callback=self.job_list,
                meta={"keyword": title, "count": 0, "plink": url},
            )

    def job_list(self, response):
        plink = response.meta["plink"].split("/")[-1]
        keyword = plink.split("-jobs")[0]
        seokeys = keyword + "-jobs"
        ids = plink.split("=")[-1]
        joburl = "https://www.naukri.com/jobapi/v3/search?noOfResults=20&urlType=search_by_keyword&searchType=adv&keyword={}&xt=catsrch&functionAreaId={}&seoKey={}&src=jobsearchDesk&latLong=".format(
            keyword, ids, seokeys
        )
        yield scrapy.Request(
            joburl,
            headers={
                "Referer": response.meta["plink"],
                "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:74.0) Gecko/20100101 Firefox/74.0",
                "appid": "109",
                "systemid": "109",
            },
            meta={
                "url": response.meta["plink"],
                "keyword": keyword,
                "ids": ids,
                "seokeys": seokeys,
            },
            callback=self.jobData,
        )

    def jobData(self, response):
        data = response.text
        data = data.replace("false", "False")
        data = data.replace("true", "True")
        jobdata = eval(data)
        if jobdata.get("jobDetails"):
            for job in jobdata["jobDetails"]:
                place = job["placeholders"]
                detail = {}
                for p in place:
                    key, value = p.values()
                    detail[key] = value
                details = {
                    "category": response.meta["keyword"],
                    "title": job["title"],
                    "jobId": job["jobId"],
                    "companyName": job["companyName"],
                    "skills": job.get("tagsAndSkills"),
                    "joburl": job["jdURL"],
                    "postedon": job["footerPlaceholderLabel"],
                    "descreption": job.get("jobDescription"),
                }
                final_result = {**detail, **details}
                yield final_result
