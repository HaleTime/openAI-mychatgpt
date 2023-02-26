import openai
from flask import redirect, render_template, request, url_for, Blueprint

import message
from chatgpt import chatgpt
from log import logger

webchat_api = Blueprint('webchat_api', __name__)


@webchat_api.route('/chat', methods=('GET', 'POST'))
def chat():
    if request.method == 'POST':
        prompt = request.form['prompt']
        logger.info(prompt)
        message.create_message(None, prompt, True, request.headers['X-Real-IP'])
        response = chatgpt(prompt)
        answer = response.choices[0].text
        logger.info(answer)
        message.create_message(None, answer, False, request.headers['X-Real-IP'])
        return redirect(url_for("chat", result=response.choices[0].text))
    result = request.args.get('result')
    return render_template("index.html", result=result)


@webchat_api.route('/image', methods=('GET', 'POST'))
def createImage():
    if request.method == 'POST':
        prompt = request.form['prompt']
        try:
            response = openai.Image.create(
                prompt=prompt,
                n=1,
                size="1024x1024"
            )
            print(response['data'][0]['url'])
            return redirect(url_for("createImage", url=response['data'][0]['url']))
        except Exception as e:
            logger.error(e)
    url = request.args.get('url')
    print(url)
    return render_template("index.html", url=url)
