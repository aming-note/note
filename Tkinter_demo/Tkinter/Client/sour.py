# -*- coding: utf8 -*-
import requests
import re
class site_link():
    #老王福利导航
    def get_url(self):
        urls = []
        url = 'http://150.95.162.90/lw78/'
        content = requests.get(url).content
        res = content.decode('utf8')
        find = re.findall(r'.*<a href=".*',res)
        for i in find:
            sp2 = re.split(r'" target="_blank"',i)
            sp3 = re.split(r'href="',sp2[0])
            url = re.findall(r'http.*',sp3[1])
            if not url:
                continue
            else:
                link1 = re.split(r'" data-kw="',url[0])
                link2 = re.split(r'["\'] target="_black"',link1[0])
                link3 = re.split(r'[\'\"]',link2[0])
                global link
                link = link3[0]
                urls.insert(-1,link+'\n')
        return urls