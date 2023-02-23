import openai
from log import logger

# 更牛逼
engine_davinci3 = "text-davinci-003"
# 更快
engine_davinci2 = "text-davinci-002"

def chat(prompt):
    try:
        response = openai.Completion.create(
            engine=engine_davinci3,
            prompt=prompt,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.6
        )
        return response
    except Exception as e:
        logger.error(e)