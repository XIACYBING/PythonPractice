# 函数由def关键字定义，按照区分，有普通函数、嵌套函数、闭包和匿名函数/lambda等
# 一个正常的方法定义如下，其中arg和return_type都是可选的
# arg参数支持默认值，如果外部调用函数时没有指定对应参数，则会直接使用默认值，
# 此外和其他语言有个很大的区别是，arg参数可以不用指定类型，类型正确与否由执行的逻辑来判断，这个特点也被称之为多态
# 这意味着任意类型的参数都可以传递进来，比如len()函数，可以传递str，也可以是其他任意的可迭代对象
# def method_name(arg...) -> return_type:
#     statement
#　　　return return_value
import textwrap
from typing import Callable


# 和其他需要编译的语言不一样，def是个可执行语句，直到函数被调用前，都是不存在的，只有在调用的时候，程序才会生成一个函数对象，并赋予名称
# todo 这里其实没有太懂，这个特性能做什么？比如我在a函数中调用b函数，但是b函数我没定义，这种代码是可行的，只有在a函数被执行的时候才会报错？
def my_func():
    print("这是普通函数")


# 此外，主程序在进行函数调用的时候，必须确保函数已经定义过了，比如下面注释的代码，就会报错，因为主程序先调用了函数，但是函数是在调用之后才定义
# 此处会报错NameError，类似变量未定义但是先使用
# pre_invoke_func()
# def pre_invoke_func():
#     pass

# 初次之外，函数之间的互相调用也需要注意，比如下面这两个函数：first_func和second_func，如果在first_func定义之后进行调用，
# 会发生报错，因为first_func方法中调用了second_func，调用时second_func还没有定义（或者说还没解释到second_func的定义）；
# 但是在second_func定义之后调用first_func，不会有任何问题，因为两个函数的定义都已经被解释了

def first_func():
    second_func()


def second_func():
    print("这是第二级函数")


# 函数还支持嵌套，比如下面这个例子，nesting_func中包含se_func，se_func中定义并调用了th_func
# 嵌套函数的优点：1、嵌套函数只能被外部函数调用和访问，如果函数内部有一些隐私数据，这种函数就可以定义为嵌套函数，确保无法被外部函数之外的其他函数调用，确保数据安全性
# 2、合理的使用嵌套函数，可以提高程序运行效率：比如我有一个递归函数，我希望对最初的入参进行检查，但是后续直接进行递归逻辑，如果是正常的函数，
# 则需要调用递归函数本身，这样子每次调用的时候，函数中都会执行一次入参校验，但是如果定义了一个嵌套递归函数，那么就可以保证入参只校验一次（当然，额外定义一个外部递归函数也能达到一样的效果，但是便利性没那么好）

def nesting_func():
    print("我是内嵌函数")

    def se_func():
        print("我是内嵌的第二层函数")

        def th_func():
            print("我是内嵌的第三层函数")
        th_func()
    se_func()


print()
nesting_func()


# 函数变量作用域：函数内的变量只能在函数中使用，无法在外部使用
# 全局变量在函数中的使用：1、全局变量在任意位置都可以被访问；
# 2、如果在函数中要修改全局变量的值，则需要用global关键字标记一下对应的全局变量（global的作用就是告诉解释器，当前变量就是外部声明的全局变量，但是不建议到处使用global，因为会让全局变量不可控）；
# 3、如果函数中定义了和全局变量一样的变量，则优先使用函数中的变量；
# 4、第二点规则中，只有immutable/不可变类型的全局变量，在函数内部修改的时候才需要用global标记，如果是mutable/可变类型的全局变量，
# 不需要global标记也能修改内部数据，比如list、tuple、set和dict等，但是如果想要对可变类型全局变量做重新赋值，则还需要global标记；
MAX_VALUE = 10


def var_scope_func():
    try:
        # 之所以要使用exec执行，因为这个SyntaxError是在解析代码阶段就抛出的异常，而不是运行代码时抛出的异常，因此try-except无法捕获
        # 此外，必须在MAX_VALE = 11之后加上global MAX_VALUE，不然函数会默认为你只是定义了一个和全局变量MAX_VALUE同名的局部变量
        # todo 确认python执行代码的阶段情况
        exec(textwrap.dedent("""
        def modify_global():
            MAX_VALUE = 11
            global MAX_VALUE
        """))
    except SyntaxError as e:
        print(f"全局变量不允许在被global标记前被变更：{e}")

    try:
        # 因为MAX_VALUE被默认为局部变量，但是发现又没有声明，因此报错
        exec(textwrap.dedent("""
        def modify_global():
            MAX_VALUE += 1
        modify_global()
        """))
    except UnboundLocalError as e:
        print(f"全局变量不允许在被标记之前变更：{e}")

    global MAX_VALUE
    MAX_VALUE = 11
    print(f"全局变量在被global标记后变更正常：{MAX_VALUE}")
    
    
def local_var_scope():
    MAX_VALUE = 'local_var'
    print(f"这是和全局变量同名的局部变量：{MAX_VALUE}")


# 嵌套函数也可以访问外部函数定义的变量，用nonlocal标记对应变量就行，nonlocal的规则和global基本一致
# todo 确认两个关键字是否有不一致的地方
def nesting_var_scope():
    outer_num = 1

    def in_scope():
        nonlocal outer_num
        print(f"我是外部函数的变量：{outer_num}")
    in_scope()


print()
var_scope_func()
print()
local_var_scope()
print()
nesting_var_scope()


# 闭包函数：就是将函数作为一个对象返回，让外部可以使用这个对象进行函数调用，类似Java的Functional
def closure_func(message):
    print(f"我是闭包函数，这是外部消息：{message}")


print()
# 将函数赋值给变量，然后使用变量进行函数调用
func = closure_func
func("发生闭包函数调用")


# 闭包函数可以让某个函数有更实际的应用，比如我有一个指数计算函数，我可以通过闭包将他变成具体的平方计算函数和立方计算函数（如果没有闭包，则需要自己额外声明更复杂的函数）
# 需要注意的是，闭包函数看似只返回了一个嵌套函数，但是实际上嵌套函数内部是可以带上外部的某些变量的，比如nth_power例子中，返回的exponent_of闭包中实际还带着外部的exponent参数
# 对于一些不经常变更的变量，我们可以通过闭包函数将其固化（比如square的2和cube的3），这个做能提高效率，增加代码可读性，并让代码变得更安全
def nth_power(exponent) -> Callable[[int], int]:
    def exponent_of(base) -> int:
        return base ** exponent
    return exponent_of


print()
# 声明平方和立方函数
square = nth_power(2)
cube = nth_power(3)
print(f"调用平方函数：{square(2)}")
print(f"调用立方函数：{cube(2)}")


if __name__ == '__main__':
    print()
    my_func()
