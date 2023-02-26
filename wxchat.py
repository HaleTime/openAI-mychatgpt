from flask import request, Blueprint

import threadlocal
from chatgpt import chatgpt
from log import logger
from login import login_interceptor
import message
import user

wxchat_api = Blueprint('wxchat_api', __name__)
algorithm = "HS256"
secret = "b10ce399d9854d7e927e8e8c96b28363"


@wxchat_api.before_request
def before():
    login_interceptor()


@wxchat_api.route('/chat', methods=['POST'])
def chat():
    prompt = request.form['prompt']
    logger.info(prompt)
    current_user = threadlocal.get_user()
    chat_num = current_user['chat_num']
    chat_limit = current_user['chat_limit']
    openid = current_user['open_id']
    if chat_limit and chat_num:
        if chat_num >= chat_limit:
            return '聊天次数用完啦~'
    # 记录聊天内容
    message.create_message(openid, prompt, True, None)
    response = chatgpt(prompt)
    answer = response.choices[0].text
    logger.info(answer)
    message.create_message(openid, answer, False, None)
    # 记录聊天次数

    user.update(None, openid, chat_num=int(chat_num)+1 if chat_num else 1)
    return answer

