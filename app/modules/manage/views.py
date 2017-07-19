from . import async
from flask import render_template
from flask import request
from app.modules.manage.spider.serializer import Serializer
from app.modules.utils.download import Downloader
from app.modules.base.base_structure import base_result
from app.modules.manage.spider.page_model import MaoyanIndexPage
import time


@async.route('/', methods=["GET", "POST"])
def index_action():

    result = base_result
    if request.method == "POST":
        serialize_page(request.form["tag"])
    result["data"] = MaoyanIndexPage.query_order_by_time()

    return render_template("manage/async.html", context=result)


def serialize_page(tag=""):
    """
    解析猫眼电影网页
    :return: 解析后的数据
    """
    downloader = Downloader(url="http://www.maoyan.com")
    page_data = downloader.download()

    serializer = Serializer(page_data)
    data = serializer.start_serialize()

    model = MaoyanIndexPage(tag=tag, created_time=time.time(), data=data)
    model.save()
