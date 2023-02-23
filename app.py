import os

import openai
from flask import Flask, render_template

from login import login_api
from message import message_api
from wxchat import wxchat_api
from webchat import webchat_api

app = Flask(__name__)
# 注册其他api到主flask里面
app.register_blueprint(message_api)
app.register_blueprint(login_api)
app.register_blueprint(wxchat_api)
app.register_blueprint(webchat_api)
openai.api_key = os.getenv("OPENAI_API_KEY")


@app.route('/', methods=['GET'])
def index():
    return render_template("index.html")


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)
