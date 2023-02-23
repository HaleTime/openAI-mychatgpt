import jwt
from flask import request, Blueprint, abort

from chatgpt import chat
from log import logger

wxchat_api = Blueprint('wxchat_api', __name__)
algorithm = "HS256"
secret = "b10ce399d9854d7e927e8e8c96b28363"


@wxchat_api.before_request
def before():
    jwt_token = request.authorization
    if jwt_token:
        try:
            # 解码 JWT token，返回字典格式的头部信息和载荷信息
            payload = jwt.decode(jwt_token, secret, algorithms=algorithm)

            # 取出 token 中的用户 ID，做进一步验证等操作
            openid = payload['openid']
            # 如果需要验证 token 是否过期等信息，也可以在这里进行验证
            # ...

            print("JWT token 验证通过")
            return

        except jwt.exceptions.InvalidSignatureError:
            abort(401, 'Unauthorized')

        except jwt.exceptions.ExpiredSignatureError:
            abort(401, 'Unauthorized')

        except jwt.exceptions.InvalidTokenError:
            abort(401, 'Unauthorized')
    else:
        print('----我走了！')
        abort(401, 'Unauthorized')


@wxchat_api.route('/chatgpt', methods=['POST'])
def chatgpt():
    prompt = request.form['prompt']
    logger.info(prompt)
    # openid = threadlocal.get_variable()
    # print(openid)
    # message.create_message(None, prompt, True, str(openid))
    response = chat(prompt)
    answer = response.choices[0].text
    logger.info(answer)
    # message.create_message(None, answer, False, str(openid))
    return answer
