from app import mongo
from mongoengine.fields import *
import time
import json


class MaoyanIndexPage(mongo.Document):
    tag = StringField(required=True)
    created_time = FloatField(default=time.time())
    data = DictField()

    @staticmethod
    def query_first_record():
        """
        查询第一条记录
        """
        result = MaoyanIndexPage.objects.order_by("-created_time").first()
        if result:
            result = json.dumps(result.data)
        return result

    @staticmethod
    def query_order_by_time(page=1, limit=10):
        """
        按时间顺序，进行分页查询数据
        :param page: 当前页
        :param limit: 每页限制数量
        :return: 数据列表
        """
        start = (page-1) * limit
        ori_result = MaoyanIndexPage.objects.order_by("-created_time")[start:start+limit]
        result = []
        for value in ori_result:
            item = dict()
            item["tag"] = value.tag
            item["time"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(value.created_time))
            result.append(item)
        return result
