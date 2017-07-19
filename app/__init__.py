from flask import Flask
from config.setting import config
from flask_mongoengine import MongoEngine

mongo = MongoEngine()


def create_app(config_name):
    """
    创建并初始化一个Flask App
    :param config_name: 初始化时使用的配置名称
    """
    app = Flask(__name__)
    # load init config obj
    app.config.from_object(config[config_name])
    # do some things when init app
    config[config_name].init_app(app)

    # init some third part by app
    mongo.init_app(app)

    # register index blueprint
    from app.modules.index import index
    app.register_blueprint(index)

    # register async blueprint
    from app.modules.manage import async
    app.register_blueprint(async, url_prefix="/manage")

    return app
