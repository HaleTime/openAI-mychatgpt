from flask import Flask, request
import openai

app = Flask(__name__)
openai.api_key = "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"
model_engine = "text-davinci-003"


@app.route('/hello', methods=['GET'])
def hello():
    prompt = request.args.get('prompt')
    completion = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5
    )
    return completion.choices[0].text


@app.route('/test', methods=['GET'])
def test():
    return "hello world"


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)
