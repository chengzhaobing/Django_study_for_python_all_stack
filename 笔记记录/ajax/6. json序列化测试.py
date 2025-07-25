import json
import decimal

info = {"name":"田曦薇", "age":20, "status":True, "type":"sex"}
v1 = json.dumps(info) # json序列化默认中文使用ASCII码形式
v2 = json.dumps(info,ensure_ascii=False)
print(v1)
print(v2)