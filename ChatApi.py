from flask import Flask,request
import openai

app = Flask(__name__)
openai.api_key="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"
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

if __name__ == '__main__':
    app.run(port=8000)