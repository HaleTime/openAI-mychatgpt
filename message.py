from flask import Blueprint
import dao.dboperate
import uuid

message_api = Blueprint('message_api', __name__)


@message_api.route('/message', methods=['GET'])
def message():
    sql = "select * from b_message"
    operator = dao.dboperate.MySqlOperator()
    messages = operator.searchbysql(sql)
    return messages


def create_message(openid, message, isMe, user_id):
    sql = "INSERT INTO b_message (id, message, is_me, user_id, open_id, chat_id) VALUES (%s, %s, %s, %s, %s, %s)"
    val = (str(uuid.uuid4()), message, 1 if isMe else 0, user_id, openid, None)
    operator = dao.dboperate.MySqlOperator()
    operatebysql = operator.operatebysql(sql, val)
    return operatebysql

