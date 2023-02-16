import os

from flask import Flask, redirect, render_template, request, url_for
import openai

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")


@app.route('/', methods=['GET'])
def index():
    return render_template("index.html")


@app.route('/chat', methods=('GET', 'POST'))
def chat():
    if request.method == 'POST':
        prompt = request.form['prompt']
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.6
        )
        print(response.choices[0].text)
        return redirect(url_for("chat", result=response.choices[0].text))
    result = request.args.get('result')
    return render_template("index.html", result=result)

@app.route('/test', methods=['GET'])
def test():
    print(os.getcwd())
    return "hello world"


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)
