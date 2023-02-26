import threading


# 创建线程本地存储对象
local_data = threading.local()


# 在一个方法中设置变量
def set_openid(openid):
    local_data.openid = openid


# 在另一个方法中获取变量
def get_openid():
    return local_data.openid

# 在一个方法中设置变量
def set_user(user):
    local_data.user = user


# 在另一个方法中获取变量
def get_user():
    return local_data.user
