import requests
from bs4 import BeautifulSoup
import json
import datetime
import os
import re
import pprint 
pp = pprint.PrettyPrinter(indent=4)


class Wisdom:
    def __init__(self,url):
        self.url=url
        self.primaryurl="https://www.wisdomjobs.com/"

    def ParsePage(self,url):
        try:
            res = requests.get(url)
            soup = BeautifulSoup(res.content,'lxml')
            return soup
        except Exception as ex:
            return None

    def GetAllJobs(self,content):
        jobscontainer = content.findAll('div', {'class': 'jobDiv'})
        jobslink=[os.path.join(self.primaryurl,j.a['href']) for j in jobscontainer if(j.find('a'))]
        return jobslink
    
    def Run(self):
        jobslinks=self.GetAllJobs(self.ParsePage(self.url))
        for j in jobslinks:
            content=self.ParsePage(j)
            Cont=content.findAll('table')
            data=self.ParseSinglePage(Cont)
            pp.pprint(data)
    
    def ParseSinglePage(self,Cont):
        try:
            for t in Cont:
                venue=[list(tds.stripped_strings) for tds in t.findAll("span",attrs={'class': 'text-muted'})]
                if (len(venue)==2) and int(re.findall(r'[\d]*',venue[-1][-1])[7])<20:
                    Li=t("li")
                    datas=[l.text for l in Li]
                    jobs={}
                    if len(datas)!=0:
                        if "Walkin" in datas[0]:
                            jobrole=datas[0].split("-")[1:]
                            full=" ".join(jobrole).split("|")[0].split("walk in for")
                            jobs['title']=full[-1]
                            jobs['company']=full[0]
                            jobs['exeprince']=datas[1]
                            jobs['city']=datas[2]
                            jobs['walkindate']=datas[3]+""+datas[4]            
                return jobs
        except:
            return None
                        
url='https://www.wisdomjobs.com/latest-walkins'
w1=Wisdom(url)
w1.Run()
        
