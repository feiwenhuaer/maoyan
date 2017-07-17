# -*- encoding:utf-8 -*-
"""
This Class is Designed to download web page with random http header and ip which can help you avoid
anti spider
"""
import re
import urllib.request
import urllib
import random

from app.modules.utils.mongo import MongoEngine
from app.modules.utils.secret import md5

HTTP_REGEX = r"http(s)?://([\w]+\.)+\w+"

USER_AGENT = ["Mozilla/5.0 (Windows NT 10.0; WOW64)", 'Mozilla/5.0 (Windows NT 6.3; WOW64)',
              'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
              'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
              'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.95 Safari/537.36',
              'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; rv:11.0) like Gecko)',
              'Mozilla/5.0 (Windows; U; Windows NT 5.2) Gecko/2008070208 Firefox/3.0.1',
              'Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070309 Firefox/2.0.0.3',
              'Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070803 Firefox/1.5.0.12',
              'Opera/9.27 (Windows NT 5.2; U; zh-cn)',
              'Mozilla/5.0 (Macintosh; PPC Mac OS X; U; en) Opera 8.0',
              'Opera/8.0 (Macintosh; PPC Mac OS X; U; en)',
              'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.12) Gecko/20080219 Firefox/2.0.0.12 Navigator/9.0.0.6',
              'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Win64; x64; Trident/4.0)',
              'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0)',
              'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2; .NET4.0C; .NET4.0E)',
              'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Maxthon/4.0.6.2000 Chrome/26.0.1410.43 Safari/537.1 ',
              'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2; .NET4.0C; .NET4.0E; QQBrowser/7.3.9825.400)',
              'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:21.0) Gecko/20100101 Firefox/21.0 ',
              'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.92 Safari/537.1 LBBROWSER',
              'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; BIDUBrowser 2.x)',
              'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/3.0 Safari/536.11']


class Downloader(object):

    cache_db = "db_spider"
    cache_col = "pages"

    def __init__(self, url="", cache=False):
        """
        You can provide url to downloaded web page
        or you can provide it before start download it
        otherwise you will receive an error
        """
        self.url = url
        self.cache = cache

        # initialize db engine
        if cache:
            self.db = MongoEngine(self.cache_db, self.cache_col)

    # close database connect
    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            self.db.close_db()
        except ValueError:
            pass

    # close database connect
    def __del__(self):
        try:
            self.db.close_db()
        except ValueError:
            pass

    @classmethod
    def valid_url(cls, url):
        """
        You can use this method to check whether the url you support is illegal
        if you don't support url it will return False directory
        :return: Bool
        """
        if not url:
            return False

        # Type Check
        if not isinstance(url, str):
            return False

        # Use regex to match the url
        regex = re.compile(HTTP_REGEX, re.IGNORECASE)

        # Return match result
        return True if regex.match(url) else False

    def download(self, coding="utf-8"):
        """
        Download web page base on the url you support in this obj
        :return:
        """
        # Check url
        if not Downloader.valid_url(self.url):
            raise ValueError("You must support download url!")

        # Get md5 url prepare for cache query and insert
        url_md5 = md5(self.url)

        if self.cache:
            cache_result = self.db.query_one({"url": url_md5})
            if cache_result:
                return cache_result.get("data", None)

        # Create a http header to avoid anti spider
        request = urllib.request.Request(url=self.url, headers={"User-Agent": random.choice(USER_AGENT)})

        # Start download page
        try:
            result = urllib.request.urlopen(request).read().decode(coding)
            if self.cache and result:
                self.db.insert_dict({"url": url_md5, "data": result})
            return result
        except:
            raise ValueError("Download web page failed!")



