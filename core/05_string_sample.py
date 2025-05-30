import statistics
import textwrap
import timeit

# 无论是用哪种方式声明的字符串，都会相等
# 不同的引号，可以让你很便利的在字符串内使用不同的引号，而不用进行转义
single_quote = 'a'
double_quote = "a"
single_triple_quote = '''a'''
double_triple_quote = """a"""
print(f"不同方式声明的字符串比较结果：{single_quote == double_quote == single_triple_quote == double_triple_quote}")


# 字符串转移声明
def escape():

    print("反斜杠的转义：\\")
    print("单引号的转义：\'")
    print("双引号的转义：\"")
    print("新的一行转义，当前是第一行；\n当前是第二行")
    print("横向制表符\t转义")
    print("纵向制表符转义：\v")

    # 这个比较特殊，能删掉一个字符，这边是冒号：被删掉
    print("退格转义：\b")


# 字符串是一个字符数组，所以大部分数组/列表的操作在字符串上都能用
def char_def():
    print()

    s = 'abcdefg'

    print(f"索引访问：{s[0]}")

    # 字符是不可变的，无法进行删改，可以新增，新增的结果是产生一个新的字符串
    try:
        s[0] = '1'
    except Exception as exception:
        print(f"字符不可变，无法操作：{exception}")
    
    print(f"字符拼接：{s + 'hijklmn'}")
    print(f"切片切割字符串：{s[::2]}")
    print(f"替换字符串：{s.replace('a', '1')}")
    num_list = '|'.join([str(x) for x in range(0, 10)])
    print(f"对可迭代对象的连接：{num_list}")
    print(f"字符串的分割：{num_list.split('|')}")
    print(f"字符串的in包含：{'a' in s}")
    print(f"字符串的find包含：{s.find('a')}")
    print(f"字符串的count包含：{s.count('a')}")
    print(f"字符串的index包含：{s.index('a')}")

    s1 = 'abababa'
    print(f"去掉字符串首尾的指定字符串：{s1.strip('a')}")
    print(f"去掉字符串首部的指定字符串：{s1.lstrip('a')}")
    print(f"去掉字符串尾部的指定字符串：{s1.rstrip('a')}")

    print("字符串函数{}".format("格式化"))
    # %表示格式化
    print("指定字符串%s，数字%d" % ("格式化", 1))


# 字符串拼接方式基准测试
def benchmark_concat():
    print()

    # 正确的缩进，需要顶到最左边，为了可读性，建议使用textwrap.dedent
    loop_concat_code = '''
s = ''
for n in range(0, 100000):
    s += str(n)
'''
    list_concat_code = textwrap.dedent('''
    l = []
    for n in range(0, 100000):
        l.append(str(n))
    s = ' '.join(l)
    ''')

    # 执行测试
    loop_time_list = timeit.repeat(stmt=loop_concat_code, number=10, repeat=5)
    list_time_list = timeit.repeat(stmt=list_concat_code, number=10, repeat=5)

    # 据说python 2.5之后，循环拼接字符串已经有了一些优化，但是看起来和直接用list拼接，效率还是有点差距
    # 平均：173.85389998089522 ms
    print(f"循环拼接字符串消耗时间：{statistics.mean(loop_time_list) * 1000} ms")

    # 平均：115.36132000619546 ms
    print(f"列表拼接字符串消耗时间：{statistics.mean(list_time_list) * 1000} ms")


if __name__ == '__main__':
    print()
    escape()
    char_def()
    benchmark_concat()
