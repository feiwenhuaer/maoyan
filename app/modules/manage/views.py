from . import async
from flask import render_template
from flask import request
from app.modules.manage.spider.serializer import Serializer
from app.modules.utils.download import Downloader

@async.route('/', methods=["GET", "POST"])
def index_action():
    serize_page()
    if request.method == "POST":
        return render_template("manage/async.html")
    else:
        return render_template("manage/async.html")


def serize_page():
    downloader = Downloader(url="http://www.maoyan.com")
    page_data = downloader.download()

    serize = Serializer(page_data)
    serize.start_serialize()

