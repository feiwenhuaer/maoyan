# -*- coding:utf-8 -*-
"""
This Class encapsulates some of the CRUD methods of MongoDB
"""

from pymongo import MongoClient

MONGODB_IP = "127.0.0.1"
MONGODB_PORT = 27017


class MongoEngine(object):

    DEFAULT_DB = "db_spider"
    DEFAULT_COL = "default_collection"

    def __init__(self, data_base, coll):
        """
        Initialize Engine with database name and collection name
        :param data_base: database name
        :param coll: collection name
        """
        # Connect to MongoDB
        self.client = MongoClient(MONGODB_IP, MONGODB_PORT)
        self.db = self.client[data_base if data_base else self.DEFAULT_DB]
        self.db.authenticate(name="client1", password="123456")
        self.col = self.db[coll if coll else self.DEFAULT_COL]

    def close_db(self):
        """
        Close connect to mongodb
        """
        self.client.close()

    def insert_dict(self, data):
        """
        You can save dict data to mongodb
        :type data: dict
        """
        # Nothing to save,it will return directory
        if not data:
            return

        # Check data type
        if not isinstance(data, dict):
            raise TypeError("The data you want to save must be the dict type")

        self.col.insert(data)

    def query_one(self, params):
        """
        Only query one obj from db,
        :type params: dict
        """
        # Check params type, mongodb only support dict type for query in python
        if not isinstance(params, dict):
            raise TypeError("The params must be support in a dictionary")

        # Query without params is meaningless
        if not params:
            raise ValueError("This is illegal to query without params")

        return self.col.find_one(params)


