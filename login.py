from flask import Blueprint, request, jsonify
import requests
import dao.dboperate
import uuid

login_api = Blueprint('login_api', __name__)
secret = "b10ce399d9854d7e927e8e8c96b28363"
app_id = "wxff2f0e20422f9e5c"


@login_api.route('/login', methods=['POST'])
def login():
    code = request.form['code']
    url = 'https://api.weixin.qq.com/sns/jscode2session?appid=' + app_id + '&secret=' + secret + '&js_code=' + code + '&grant_type=authorization_code'
    response = requests.get(url)
    openid = response.json()['openid']
    session_key = response.json()['session_key']
    print('openid:' + openid, 'session_key:' + session_key)
    search = f'select * from b_user where open_id = \'{openid}\''
    operator = dao.dboperate.MySqlOperator()
    searchbysql = operator.searchbysql(search)
    if any(searchbysql):
        return jsonify({'openid': openid, 'session_key': session_key})
    sql = 'INSERT INTO b_user (id, open_id, session_key) VALUES (%s, %s, %s)'
    val = (str(uuid.uuid4()), openid, session_key)
    operator = dao.dboperate.MySqlOperator()
    operator.operatebysql(sql, val)
    return 'success'
