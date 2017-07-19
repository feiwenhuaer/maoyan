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
        # only_content_div = SoupStrainer("body")
        self.obj = BeautifulSoup(data, features="lxml", from_encoding=self.encoding)

    def start_serialize(self):
        result = dict()
        # 解析banner
        result["banner_list"] = self.serialize_banner(self.obj.find("div", class_="banner"))
        # 解析侧边栏 - 今日票房
        result["aside"] = self.serialize_aside(self.obj.find("div", class_="aside"))
        # 解析主体内容
        result["panel"] = self.serialize_panel(self.obj.find("div", class_="movie-grid"))
        return result

    def serialize_panel(self, grid_div):
        """
        解析页面主体
        """
        result = []
        if not grid_div:
            return result

        panel_list = grid_div.find_all("div", class_="panel")
        for panel_div in panel_list:
            item = dict()
            item["head"] = self.serialize_header(panel_div.find("div", class_="panel-header"))
            item["content"] = self.serialize_movie_list(panel_div.find_all("dd"))
            result.append(item)

        return result

    @staticmethod
    def serialize_movie_list(dd_list):
        result = []
        if not dd_list:
            return result

        for dd in dd_list:
            item = dict()
            item["url"] = dd.find("a").get("href")
            item["movie_id"] = dd.find("a").get("data-val")
            item["bg_url"] = dd.find("img", class_="poster-default").find_next("img").get("data-src")
            item["movie-title"] = dd.find("div", class_="movie-title").string
            result.append(item)

        return result

    @staticmethod
    def serialize_banner(banner_div):
        result = []
        if not banner_div:
            return result

        a_list = banner_div.find_all("a")
        for a in a_list:
            if not a:
                continue

            bg_url = a.get("data-bgurl")
            if not bg_url:
                continue

            result.append({
                "bg_url": bg_url,
                "href": a.get("href")
            })

        return result

    def serialize_aside(self, aside_div):
        """
        解析侧边栏
        """
        result = {
            "ranking": {},
            "total": {},
            "expect": {},
            "top100": {}
        }

        if not aside_div:
            return result

        result["ranking"] = self.serialize_ranking(aside_div.find("div", class_="ranking-box-wrapper"))
        result["total"] = self.serialize_total(aside_div.find("div", class_="box-total-wrapper clearfix"))
        result["expect"] = self.serialize_expect(aside_div.find("div", class_="most-expect-wrapper"))
        result["top100"] = self.serialize_top(aside_div.find("div", class_="top100-wrapper"))
        return result

    def serialize_top(self, top_div):
        """
        解析TOP100榜单
        """
        result = {
            "head": {},
            "content": [],
        }
        if not top_div:
            return result

        result["head"] = self.serialize_header(top_div.find("div", class_="panel-header"))
        result["content"] = self.serialize_top_content(top_div.find("div", class_="panel-content"))

        return result

    @staticmethod
    def serialize_top_content(content_div):
        """
        解析TOP100中的主体内容
        """
        result = []
        if not content_div:
            return result

        li_list = content_div.find_all("li")
        for index, li in enumerate(li_list):
            a_div = li.find("a")
            if not a_div:
                continue
            item = dict()
            item["url"] = a_div.get("href")
            item["movie_id"] = a_div.get("data-val")

            rank_index = a_div.find("i", class_="ranking-index")
            item["rank"] = rank_index.string if rank_index else ""

            name_div = a_div.find("span", class_="ranking-movie-name")
            item["movie_name"] = name_div.string if name_div else ""

            item["grade"] = a_div.find("span", class_="stonefont").string

            img_div = a_div.find("img", class_="ranking-img default-img")
            src = img_div.get("data-src") if img_div else ""
            if not src:
                src = img_div.get("src") if img_div else ""
            item["rank_img"] = src

            if index == 0:
                item["movie_name"] = a_div.find("span", class_="ranking-top-moive-name").string

            result.append(item)

        return result

    def serialize_expect(self, expect_div):
        """
        解析最受期待榜单
        """
        result = {
            "head": {},
            "content": [],
        }
        if not expect_div:
            return result

        result["head"] = self.serialize_header(expect_div.find("div", class_="panel-header"))
        result["content"] = self.serialize_expect_content(expect_div.find("div", class_="panel-content"))

        return result

    @staticmethod
    def serialize_expect_content(content_div):
        """
        解析最受期待帮点中的主体内容
        """
        result = []
        if not content_div:
            return result

        li_list = content_div.find_all("li")
        for index, li in enumerate(li_list):
            a_div = li.find("a")
            if not a_div:
                continue
            item = dict()
            item["url"] = a_div.get("href")
            item["movie_id"] = a_div.get("data-val")

            rank_index = a_div.find("i", class_="ranking-index")
            item["rank"] = rank_index.string if rank_index else ""

            name_div = a_div.find("span", class_="ranking-movie-name")
            item["movie_name"] = name_div.string if name_div else ""

            item["expect_num"] = a_div.find("span", class_="stonefont").string

            img_div = a_div.find("img", class_="ranking-img default-img")
            src = img_div.get("data-src") if img_div else ""
            if not src:
                src = img_div.get("src") if img_div else ""
            item["rank_img"] = src

            item["release_time"] = ""
            if index == 0:
                item["movie_name"] = a_div.find("span", class_="ranking-top-moive-name").string
                item["release_time"] = a_div.find("p", class_="ranking-release-time").string
            if not item["movie_name"]:
                item["movie_name"] = a_div.find("div", class_="name-link ranking-movie-name").string
            result.append(item)

        return result

    @staticmethod
    def serialize_total(total_div):
        result = dict()
        if not total_div:
            return result

        result["title"] = total_div.find("h3").string
        result["total"] = total_div.find("span", class_="stonefont").string
        result["more_link"] = total_div.find("a", class_="more").get("href")
        return result

    def serialize_ranking(self, rank_div):
        result = {
            "head": {},
            "content": [],
        }

        if not rank_div:
            return result

        # 解析panel的头部数据
        result["head"] = self.serialize_header(rank_div.find("div", class_="panel-header"))
        result["content"] = self.serialize_rank_content(rank_div.find(class_="panel-content"))

        return result

    @staticmethod
    def serialize_rank_content(content_div):
        result = []
        if not content_div:
            return result

        li_list = content_div.find_all("li")
        for index, li in enumerate(li_list):
            a_div = li.find("a")
            if not a_div:
                continue

            item = dict()

            item["movie_id"] = a_div["data-val"]
            item["url"] = a_div["href"]
            item["intro_img"] = ""

            if index == 0:
                item["rank"] = "1"
                item["intro_img"] = a_div.find("img", class_="ranking-img").get("data-src")
                item["movie_name"] = a_div.find("span", class_="ranking-top-moive-name").string
            else:
                item["rank"] = a_div.find("i", class_="ranking-index").string
                item["movie_name"] = a_div.find("span", class_="ranking-movie-name").string

            item["rank_num"] = a_div.find("span", class_="stonefont").string

            result.append(item)

        return result

    @staticmethod
    def serialize_header(div):
        """
        通用头部解析
        """
        result = {
            "title": "",
            "more": "",
        }

        if not div:
            return result

        panel_title = div.find(class_="panel-title")
        if panel_title:
            title = panel_title.find("span").string
            result["title"] = title if title else ""

        panel_more = div.find(class_="panel-more")
        if panel_more:
            url = panel_more.find("a")
            if url:
                more = dict()
                more["more_url"] = url.get("href")
                more["more_title"] = url.find("span").string
                result["more"] = more

        return result
