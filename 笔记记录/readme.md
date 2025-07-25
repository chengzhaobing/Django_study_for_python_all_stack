# 项目说明

## 1. 切换登录验证码方式

* 数字验证码
> 更改app02 -- utils -- code.py  ----为数字验证码
return str(random.randint(0,9))  

* 英文验证码
> 生成随机字母 ----- 字母验证码
return chr(random.randint(65, 90))
        