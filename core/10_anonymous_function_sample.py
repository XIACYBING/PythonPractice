# 匿名函数，一般是指lambda，格式如下：
# lambda argument1, argument2,... argumentN : expression
# lambda是关键字，argument是参数定义，expression中会使用前面声明的argument，但是需要注意的是，lambda的表达式只支持一行
# lambda只专注于简单的任务，因此只能一行表达式，详情见python之父的解释：https://www.artima.com/weblogs/viewpost.jsp?thread=147358
# 而且需要注意的是，lambda需要的是表达式/expression，而不是语句/statement，表达式代表需要使用一系列公式去表达一个东西（比如平方计算），
# 而语句则是完成了某些功能（比如print的打印，x = 1的赋值）
from functools import reduce
from tkinter import Button, mainloop

# 比如下面这两个例子
square = lambda x: x ** 2
cube = lambda x: x ** 3
print(f"使用lambda进行的平方计算：{square(2)}")
print(f"使用lambda进行的立方计算：{cube(2)}")


# lambda可以作为列表元素而存在，常规def函数不行（闭包是否可以？）
# todo 常规def函数不能作为列表元素而存在，这个是指不能在列表中定义def函数吧？如果把def函数作为闭包放入列表，目前实测是可行的
# todo 确认lambda和常规函数的区别
def square_f(base) -> int:
    return base ** 2


square_func = square_f

func_list = [square, square_func]
[print(f"在推导式中使用lambda/闭包进行计算：{x(2)}") for x in func_list]


# lambda在Tkinter GUI中的应用，会出现一个按钮，点击之后就会在控制台输出begin pressed，如果不用lambda，我们就需要额外定义一个函数
def tkinter_sample():
    button = Button(text='this is a button', command=lambda: print('begin pressed'))
    button.pack()
    mainloop()


# tkinter_sample()

# lambda主要有两个作用，减少复杂度和提高可读性；常规函数是为了减少重复性和模块化代码而被定义出来，
# 但是如果有一个简单的任务（比如说平方计算），只会被调用一次，这时候还有必要给它一个定义和函数名称吗？匿名函数/lambda是更好的选择


print()
# 这里介绍几个常用lambda的函数，和Java的Stream相关函数类型
# 需要注意的是，虽然很多功能，map/filter和推导式都能做到，map和filter的实现是C语言编写的，省略了解释的环节，因此效率会更胜一筹

# map(function, iterable)，传入一个函数（一般是匿名函数）和一个可迭代对象，可迭代对象中的每个元素都会传入函数中执行一次，最终返回另一个可迭代对象
print(f"使用map后: {list(map(lambda x: x ** 2, [1, 2, 3]))}")

# filter(function, iterable)，和map类型，传入一个函数（函数需要返回true或false）和一个可迭代对象，可迭代对象中的每个元素都会传入函数中执行一次，
# 函数会返回True和False，如果是True，元素则保留，反之则丢弃，最终返回一个保留元素的迭代器
print(f"使用filter后：{list(filter(lambda x: x % 2 == 0, range(10)))}")

# reduce(function, iterable)，和另外两个函数相比，reduce要求传入的函数，它的入参要有两个，一个是当前元素，一个是前置元素的处理结果
print(f"使用reduce进行一到十的相加后：{reduce(lambda x, amount: amount + x, range(11))}")


# 思考题：字典值倒序排序
def thinking():
    print()
    d = {'mike': 10, 'lucy': 2, 'ben': 30}
    print(f"根据字典值进行倒序排序：{dict(sorted(d.items(), key=lambda item: item[1], reverse=True))}")


thinking()


if __name__ == '__main__':
    pass
