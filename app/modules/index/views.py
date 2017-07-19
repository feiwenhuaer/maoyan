from . import index
from flask import render_template
from app.modules.manage.spider.page_model import MaoyanIndexPage
from app.modules.base.base_structure import base_result


@index.route('/')
def index_action():

    result = base_result
    result["data"] = MaoyanIndexPage.query_first_record()

    return render_template("index/index.html", context=result)


