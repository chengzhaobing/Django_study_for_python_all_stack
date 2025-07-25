

# 面向对象的基础知识


class T1(object):
    pass

TXW1 = T1() #实例化一个对象
print(TXW1) #打印对象
# 打印结果为一个对象:
# <__main__.TianXiWei object at 0x000001BE33502C70>



class T2(object):
    def __str__(self):
        return "cheng love TXW"

TXW1 = T2() #实例化一个对象
print(TXW1) #打印对象


# 打印结果为对象内的内容: cheng love TXW


class T3(object):
    def __init__(self,name):
        self.name = name

    def __str__(self):
        return self.name

obj1 = T3("IT部门")
obj2 = T3("市场部门")
print(obj1)
print(obj2)

# 打印封装好的内部的某个值