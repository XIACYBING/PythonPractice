from copy import deepcopy

# 列表是动态的，长度可变，可以随意的增加、删减或改变元素。列表的存储空间略大于元组，性能略逊于元组。
# 元组是静态的，长度大小固定，不可以对元素进行增加、删减或者改变操作。元组相对于列表更加轻量级，性能稍优。

# 定义一个列表，列表长度可变，可以增减替换元素
# 列表在不需要使用的时候会被垃圾回收
list_sample = [1, "2", 3.0]

# 定义一个元组，元组长度不可变，无法增减替换元素，如果要变更，只能新建一个元组
# 静态元组更可能被缓存，不会被垃圾回收，以便下次直接使用
tuple_sample = (1, "2", 3.0)


# 展示列表新建的各种方法
def list_new():

    print("开始展示列表新建的各种方法")

    # 列表推导式新建
    new_list = [x for x in list_sample]
    print(f"推导式新建：{new_list}")

    # 切片新建
    new_list = list_sample[:]
    print(f"切片新建：{new_list}")

    # 组合新建
    print(f"组合新建：{[1, '2', 3.0] + [4.0]}")

    # 重复新建
    print(f"重复新建：{[5] * 4}")

    # copy
    new_list = list_sample.copy()
    print(f"copy新建：{new_list}")

    # deepcopy：深拷贝，对于元素也进行了拷贝
    new_list = deepcopy(list_sample)
    print(f"deepcopy新建：{new_list}")

    print(f"列表推导式新建指定长度的空列表{[None for _ in range(3)]}")

    print("列表新建方法展示结束\n")


# 展示列表其他的常用方法
def list_def():

    print("开始展示列表常用的各种方法")

    print(f"统计元素出现次数：{list_sample.count(1)}")

    # 元素不存在会报错
    print(f"查找元素出现的第一个位置：{list_sample.index('2')}")

    list_sort = [11, 2, 153, 4, 665]
    list_sort.sort()
    print(f"列表原地排序：{list_sort}")

    list_sort.reverse()
    print(f"列表原地倒序：{list_sort}")

    print(f"列表排序：{sorted(list_sort)}")

    # reversed方法返回的是个迭代器，需要重新转换成列表
    print(f"列表倒序{list(reversed(list_sort))}")

    print()


# todo 展示列表新增元素的各种方法


# 展示列表移除元素的各种方法
def list_remove():

    print("开始展示列表移除元素的各种方法")

    list_remove_sample = list_sample[:]

    # 列表推导式移除，最后生成一个新列表：expression for item in iterable if condition
    print(f"列表推导式移除：{[x for x in list_remove_sample if x != '2']}")

    # 基于元素移除：remove
    list_remove_sample.remove(1)
    print(f"remove移除：{list_remove_sample}")

    # 基于索引移除：pop、del
    list_remove_sample.pop(0)
    print(f"pop移除：{list_remove_sample}")
    del list_remove_sample[0]
    print(f"del移除：{list_remove_sample}")

    print("列表移除元素方法展示结束\n")


# todo 展示列表修改元素的各种方法
def list_modify():

    print("开始展示列表修改元素的各种方法")

    print()


# 展示列表查询元素的各种方法
def list_query():

    print("开始展示列表查询元素的各种方法")

    # 正数索引访问
    print(f"正数索引访问：{list_sample[0]}")

    # 负数索引访问
    print(f"付数索引访问：{list_sample[-1]}")

    # 切片访问：startIndex:step
    print(f"切片访问：{list_sample[0:2]}")

    # 元素访问
    print(f"元素访问：{1 in list_sample}")

    # 遍历访问
    for item in list_sample:
        print(f"遍历访问：{item}")

    # enumerate访问
    for index, item in enumerate(list_sample):
        print(f"遍历访问，索引：{index}，元素：{item}")
    print()

# todo 展示元组新建的各种方法


# 展示元组增加元素的各种方法
# noinspection PyTupleItemAssignment,PyUnresolvedReferences
def tuple_add():

    print("元组增加元素：元组不支持直接增加元素，可以添加一个元素生成一个新元组")

    # 异常场景
    try:
        tuple_sample[0] = 40
    except Exception as exception:
        print(f"元组元素重分配异常：：{exception}")

    # 添加元素，新建一个新元组
    print(f"添加元素，新建一个新元组：{tuple_sample + (1, )}")


# todo 展示元组删除元素的各种方法
# todo 展示元组修改元素的各种方法
# todo 展示元组查询元素的各种方法


if __name__ == '__main__':

    list_new()
    list_def()
    list_remove()
    list_query()
    tuple_add()
