from bs4 import BeautifulSoup
from bs4 import UnicodeDammit
from bs4 import SoupStrainer
import re


class Serializer(object):

    def __init__(self, data, encoding=None):
        """
         Initialize serializer class
         :param data: ori data
         :param encoding: encoding type of your ori data
         """
        self.data = data

        if not self.data:
            raise ValueError("You must input origin data to this class")

        # if you don't support encoding type we will use chardet to check the type
        self.encoding = encoding if encoding else UnicodeDammit(self.data).original_encoding
        self.encoding = None if self.encoding == "utf-8" else self.encoding

        # initialize beautiful soup
        only_content_div = SoupStrainer("body")
        self.obj = BeautifulSoup(data, features="lxml", from_encoding=self.encoding, parse_only=only_content_div)

    def start_serialize(self):
        self.serialize_banner()

    def serialize_banner(self):
        banner = self.obj.find("div", class_="slick-track")
        a_list = banner.find_all("a")
        for a in a_list:
            print(a)