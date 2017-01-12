# -*- coding:utf-8 -*-
import scrapy
from scrapy.selector import Selector
from scrapy.http import Request,FormRequest
import sys


reload(sys)
sys.setdefaultencoding("utf8")


class DmozSpider(scrapy.Spider):
    repoId = "6"

    name = "jira"
    allowed_domains = ["k2data.com.cn"]

    start_urls = [
        "http://jira.k2data.com.cn/secure/bbb.gp.gitviewer.BrowseGit.jspa?repoId="
        + repoId
        + "&branchName=master&tagName&commitId&path"
    ]

    def start_requests(self):
        print("start..................")
        return [FormRequest(
            "http://jira.k2data.com.cn/login.jsp",
            formdata={'os_username': '',
                      'os_password': ''
                      },
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.57 Safari/537.36'},
            method='POST',
            callback=self.after_login
        )]

    def after_login(self, response):
        print "callback......................"
        for url in self.start_urls:
            yield self.make_requests_from_url(url)

    def parse(self, response):
        hxs = Selector(response)
        items = []

        divs = hxs.xpath('//div[@class="bbb-gp-gitviewer-files-list__row"]')

        print(divs)