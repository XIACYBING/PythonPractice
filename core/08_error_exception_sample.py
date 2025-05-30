# 错误一般是指语法错误，编译器一般会报错：SyntaxError
# if '' is None
#   print()
import random
import sys
import traceback


def division_by_zero():
    1 / 0


def name_error():
    print(order * 2)


# python异常：https://docs.python.org/3/library/exceptions.html#bltin-exceptions
# 异常则是指语法正确，但是执行错误导致抛出异常的情况，比如下面这种
try:
    division_by_zero()
except Exception as exception:
    print(f"发现除零异常：{exception}")

# 在用except捕获异常时，需要注意异常的类型，except只会捕获指定的异常
try:
    try:
        division_by_zero()
    except NameError as e:
        pass
except ZeroDivisionError as err:
    print(f"外层捕获到异常：{err}")


def random_error():
    if random.randint(0, 1):
        division_by_zero()
    else:
        name_error()


# 如果在一串代码中有多种异常可能抛出，则可以都捕获，有三种方法
# 两个异常都在一个except中捕获
try:
    random_error()
except (ZeroDivisionError, NameError) as e:
    print(f"捕获到异常：{e}")

# 两个异常在两个except中捕获
try:
    random_error()
except ZeroDivisionError as e:
    print(f"捕获到除零异常：{e}")
except NameError as e:
    print(f"捕获到命名异常：{e}")

# 声明Exception（所有非系统异常的基类，能匹配任意非系统异常），捕获所有异常
try:
    random_error()
except Exception as e:
    print(f"捕获到异常：{e}")

# 在不需要打印异常具体信息的时候，也可以只声明except，但是这种方式比较不建议
try:
    random_error()
except:
    # sys可以获取当前的异常
    print(f"发现异常：{sys.exc_info()[0]}")


# 声明Exception（所有非系统异常的基类，能匹配任意非系统异常），捕获所有异常
try:
    random_error()
except Exception as e:
    print("捕获到异常：{}".format(e))


# 初次之外，还可以在finally中做一些收尾处理
try:
    random_error()
except Exception as ex:
    # 直接输出堆栈错误信息
    traceback.print_exc()

    # 堆栈错误信息作为字符串返回
    print(f"打印详细堆栈信息：{traceback.format_exc()}")
finally:
    print("到达finally模块")


# 自定义异常
class MyError(Exception):
    def __init__(self, value):
        self.value = value


try:
    raise MyError("自定义异常的错误信息")
except MyError as e:
    print(f"发现自定义异常：{e}")


if __name__ == '__main__':
    pass
