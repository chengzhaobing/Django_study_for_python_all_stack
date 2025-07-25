import hashlib

from django.conf import settings

""" 数据库密码字段加密 """
def md5(data_string):
    # 这里不加盐salt settings提供了一个密文
    obj = hashlib.md5(settings.SECRET_KEY.encode('utf-8'))
    obj.update(data_string.encode('utf-8'))
    return obj.hexdigest()