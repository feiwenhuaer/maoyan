from . import index
from flask import render_template


@index.route('/')
def index_action():
    return render_template("index/index.html")


