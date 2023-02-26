import dao.dboperate
import uuid


def get(id, openid):
    sql = 'select * from b_user where 1=1 '
    if id:
        sql = sql + f' and id = \'{id}\''
    if openid:
        sql = sql + f' and open_id = \'{openid}\''

    operator = dao.dboperate.MySqlOperator()
    return operator.searchbysql(sql)


def create(user_name, phone, openid, session_key, last_login_time, chat_limit, chat_num):
    sql = "INSERT INTO b_user (id, user_name, phone, open_id, session_key, last_login_time, chat_limit, chat_num) " \
          "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    val = (str(uuid.uuid4()), user_name, phone, openid, session_key, last_login_time, chat_limit, chat_num)
    operator = dao.dboperate.MySqlOperator()
    return operator.operatebysql(sql, val)


def update(id, openid, **kwargs):
    updatelist = []
    val = []
    for key, value in kwargs.items():
        updatelist.append(f' {key} = %s ')
        val.append(value)
    updatesql = 'UPDATE b_user SET ' + ' AND '.join(updatelist) + ' where '
    if id:
        updatesql = updatesql + f'id = \'{id}\''
    else:
        if openid:
            updatesql = updatesql + f'open_id = \'{openid}\''
    print(updatesql)
    operator = dao.dboperate.MySqlOperator()
    return operator.operatebysql(updatesql, val)