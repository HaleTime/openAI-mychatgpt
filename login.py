from flask import Blueprint, request, abort
import requests
import dao.dboperate
import uuid
import jwt
import time
import threadlocal
import user

login_api = Blueprint('login_api', __name__)
secret = "b10ce399d9854d7e927e8e8c96b28363"
app_id = "wxff2f0e20422f9e5c"
algorithm = "HS256"


def login_interceptor():
    jwt_token = getToken()
    if jwt_token:
        try:
            print(jwt_token)
            # 解码 JWT token，返回字典格式的头部信息和载荷信息
            payload = jwt.decode(jwt_token, secret, algorithms=[algorithm])

            # 取出 token 中的用户 ID，做进一步验证等操作
            openid = payload['openid']
            current_user = user.get(None, openid)[0]
            threadlocal.set_user(current_user)
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


@login_api.route('/login', methods=['POST'])
def login():
    code = request.form['code']
    if not code:
        return abort(401, 'Code can not be None!')
    url = 'https://api.weixin.qq.com/sns/jscode2session?appid=' + app_id + '&secret=' + secret + '&js_code=' + code + '&grant_type=authorization_code'
    response = requests.get(url)
    openid = response.json()['openid']
    session_key = response.json()['session_key']
    current_timestamp = int(time.time())
    auth_info = {'openid': openid, 'session_key': session_key, 'current_timestamp': current_timestamp}
    print(auth_info)
    search = f'select * from b_user where open_id = \'{openid}\''
    operator = dao.dboperate.MySqlOperator()
    searchbysql = operator.searchbysql(search)
    jwt_token = jwt.encode(auth_info, secret, algorithm=algorithm)
    print(jwt_token)
    if any(searchbysql):
        return jwt_token
    sql = 'INSERT INTO b_user (id, open_id, session_key) VALUES (%s, %s, %s)'
    val = (str(uuid.uuid4()), openid, session_key)
    operator = dao.dboperate.MySqlOperator()
    operator.operatebysql(sql, val)
    return jwt_token


# 手动解析token，request.authorization只支持基于 HTTP Basic Auth 的认证信息
def getToken():
    auth_header = request.headers.get("Authorization")
    if auth_header:
        try:
            auth_token = auth_header.split(" ")[1]
        except IndexError:
            return "Invalid token supplied", 401
    else:
        auth_token = None
    return auth_token