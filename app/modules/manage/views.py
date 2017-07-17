from . import async
from flask import render_template


@async.route('/')
def index_action():
    return render_template("manage/async.html")
