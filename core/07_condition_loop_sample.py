import random


# 条件说明
def condition():
    print()

    if random.randint(0, 1):
        print(f"这是{True}")
    else:
        print(f"这是{False}")

    num = random.randint(0, 3)
    if num == 0:
        print("这是0")
    elif num == 1:
        print("这是1")
    else:
        print(f"这是{num}")

    # 字符串中，空字符串是False，非空字符串是True
    if not '':
        print("空字符串是False")

    # int中，0是False，其他值是True
    if not 0:
        print("0是False")

    # list/tuple/dict/set中，空对象是False，非空对象是true
    if not {}:
        print("空迭代对象是False")

    # 对象中，None是False，其他的是True
    if not None:
        print("None是False")


# 循环说明
def loop():
    print()

    # 可迭代对象（list/tuple/dict/set）都可以迭代
    for i in list([1]):
        print(f"list循环：{i}")
    for i in tuple([2]):
        print(f"tuple循环：{i}")
    for i in {1}:
        print(f"set循环：{i}")
    for key in dict({1: 1}):
        print(f"dict的key循环：{key}")
    
    # 需要注意，dict直接进行循环的话，参与循环的只是它的key，可以通过item()让key-value键值对参与循环，或者通过values()让value进行循环
    for item in dict({1: 2}).items():
        print(f"dict的键值对循环，key：{item[0]}，value：{item[1]}")
    for value in dict({1: 2}).values():
        print(f"dict的值循环：{value}")

    # 索引循环：list和tuple都支持索引访问
    sample_list = [1, 2, 3]
    for index in range(0, len(sample_list)):
        print(f"索引：{index}，对应元素是：{sample_list[index]}")

    # 同时需要索引和元素的循环，将其转成枚举再循环
    for index, element in enumerate(sample_list):
        print(f"索引：{index}，对应元素是：{element}")

    # 带上continue和break的循环
    for ele in sample_list:
        if ele == 1:
            continue
        if ele == 3:
            break
        print(f"当前元素是：{ele}")

    # while循环，只要条件满足就一直执行，也可以进行continue和break
    while_sample = [1, 2, 3, 4]
    index = 0
    i = while_sample[index]
    while i < 3:
        print(f"while循环，当前元素是：{i}")
        index += 1
        i = while_sample[index]


# 循环可以简化为推导式
def comprehension():
    print()

    # 推导式：expression1 if condition else expression2 for item in iterable
    # 推导式：expression1 for item in iterable if condition
    # 推导式：expression1 for item in iterable
    com_sample = [1, 2, 3, 4]
    [print(f"这是单数：{ele}") if ele % 2 == 1 else print(f"这是双数：{ele}") for ele in com_sample]
    print()
    [print(f"这是小于3的数字：{ele}") for ele in com_sample if ele < 3]
    print()
    [print(f"这是列表元素：{ele}") for ele in com_sample]

    # 多可迭代对象推导式（将x_list和y_list的每个元素进行笛卡尔积组合）：expression for x in x_list for y in y_list
    # expression for x in x_list for y in y_list if condition
    # expression1 if condition else expression2 for x in x_list for y in y_list
    x_list = [1, 2, 3]
    y_list = [4, 5, 6]
    [print(f"x: {x}, y: {y}") for x in x_list for y in y_list]
    print()
    [print(f"x: {x}, y: {y}") for x in x_list for y in y_list if x > 2 and y > 5]
    print()
    [print(f"x: {x}, y: {y}") if x > 2 and y > 5 else print("不符合条件") for x in x_list for y in y_list]

    # 在推导式中，expression也可以是一个推导式，也就是推导式嵌套
    print(f"嵌套推导式返回列表集合：{[[y for y in y_list if y > 4] for x in x_list if x > 1]}")

    # 字典推导式，适合快速生成字典
    # 需要注意的是，下面这个例子中，x_list和y_list组成了笛卡尔积，但是因为在dict中，相同key的value会被覆盖，所以最终只保留{1: 6, 2: 6, 3: 6}
    dict_sample = {x: y for x in x_list for y in y_list}
    print(f"字典推导式：{dict_sample}")

    # 集合推导式：和列表推导式基本一致，区别只是在于它使用的是{}，且会被去重
    duplicate_ele_list = [1, 1, 2, 2, 3, 3]
    ele_set = {x for x in duplicate_ele_list}
    print(f"集合推导式：{ele_set}")


# 思考题实现
def thinking():
    """
    最后给你留一个思考题。给定下面两个列表attributes和values，要求针对values中每一组子列表value，输出其和attributes中的键对应后的字典，最后返回字典组成的列表。
    attributes = ['name', 'dob', 'gender']
    values = [['jason', '2000-01-01', 'male'], ['mike', '1999-01-01', 'male'], ['nancy', '2001-02-01', 'female']]

    # expected output:
    [{'name': 'jason', 'dob': '2000-01-01', 'gender': 'male'},
    {'name': 'mike', 'dob': '1999-01-01', 'gender': 'male'},
    {'name': 'nancy', 'dob': '2001-02-01', 'gender': 'female'}]
    你能分别用一行和多行条件循环语句，来实现这个功能吗？
    """

    expect_result = [{'name': 'jason', 'dob': '2000-01-01', 'gender': 'male'},
                     {'name': 'mike', 'dob': '1999-01-01', 'gender': 'male'},
                     {'name': 'nancy', 'dob': '2001-02-01', 'gender': 'female'}]

    attributes = ['name', 'dob', 'gender']
    values = [['jason', '2000-01-01', 'male'], ['mike', '1999-01-01', 'male'], ['nancy', '2001-02-01', 'female']]

    # 嵌套推导式实现
    actual_result = [dict(zip(attributes, value)) for value in values]
    print(actual_result == expect_result)

    # 嵌套推导式-索引实现
    actual_result = [dict([(attributes[index], value[index]) for index in range(len(value))]) for value in values]
    print(actual_result == expect_result)

    # 嵌套推导式-索引-内层字典推导式实现
    actual_result = [{attributes[index]: value[index] for index in range(len(value))} for value in values]
    print(actual_result == expect_result)

    # 内部类似zip函数，比较复杂
    actual_result = [dict((attr, val) for attr, val in list(map(lambda x, y: (x, y), attributes, value)))
                     for value in values]
    print(actual_result == expect_result)

    # 多层循环实现
    actual_result = []
    for value in values:
        result = {}
        for index in range(len(value)):
            result[attributes[index]] = value[index]
        actual_result.append(result)
    print(actual_result == expect_result)


if __name__ == '__main__':
    condition()
    loop()
    comprehension()
    thinking()
