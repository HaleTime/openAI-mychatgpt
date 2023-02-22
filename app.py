import os

from flask import Flask, redirect, render_template, request, url_for
import openai
import log

import MessageApi
from MessageApi import message_api
from login import login_api


app = Flask(__name__)
# 注册其他api到主flask里面
app.register_blueprint(message_api)
app.register_blueprint(login_api)
openai.api_key = os.getenv("OPENAI_API_KEY")


# @Limiter.limiter("1 per minute")
@app.route('/', methods=['GET'])
def index():
    return render_template("index.html")


@app.route('/chat', methods=('GET', 'POST'))
def chat():
    if request.method == 'POST':
        prompt = request.form['prompt']
        log.logger.info(prompt)
        MessageApi.create_message(None, prompt, True)
        response = chatbyapikey(prompt)
        answer = response.choices[0].text
        log.logger.info(answer)
        MessageApi.create_message(None, prompt, False)
        return redirect(url_for("chat", result=response.choices[0].text))
    result = request.args.get('result')
    return render_template("index.html", result=result)


@app.route('/image', methods=('GET', 'POST'))
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
            logging.error(e)
    url = request.args.get('url')
    print(url)
    return render_template("index.html", url=url)

@app.route('/chatgpt', methods=['POST'])
def chatgpt():
    prompt = request.form['prompt']
    print(prompt)
    response = chatbyapikey(prompt)
    print(response.choices[0].text)
    return response.choices[0].text


@app.route('/chatgpt', methods=['GET'])
def chatgptget():
    prompt = request.args.get('prompt')
    print(prompt)
    response = chatbyapikey(prompt)
    print(response.choices[0].text)
    return response.choices[0].text


def chatbyapikey(prompt):
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.6
        )
        return response
    except Exception as e:
        logging.error(e)





if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)
