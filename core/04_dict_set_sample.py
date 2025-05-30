import statistics
import time
import timeit

# 字典是一系列的键值对，有序，长度可变，元素可进行增删改查
# 查询时间复杂度为O(1)，键值类型不限制，底层基于哈希表实现，键唯一
# 从3.7开始有序，3.6无法保证有序，3.6之前是无需
dict_sample = {'name': 'jason', 'age': 20, 'gender': 'male'}

# 集合是一系列无序、唯一的元素组合，相关操作和字典基本一样，集合本质上也是一个字典，不过对外操作的只有字典的key
set_sample = {1, 2, 3}


# 展示字典的各种方法
def dict_example():
    
    print(f"直接初始化：{dict_sample}")

    print(f"dict方法-JSON初始化：{dict({'name': 'jason', 'age': 20, 'gender': 'male'})}")

    print(f"dict方法-集合初始化：{dict([('name', 'jason'), ('age', 20), ('gender', 'male')])}")
    
    print(f"dict方法-可变参数初始化：{dict(name='jason', age=20, gender='male')}")

    print(f"dict方法-可迭代对象初始化：{dict(dict_sample)}")

    print()

    print(f"直接通过key访问：{dict_sample['name']}")

    # key不存在则会抛出异常
    try:
        dict_sample['non']
    except Exception as exception:
        print(f"捕获到key不存在的异常：{exception}")

    print(f"key不存在时可用get方法：{dict_sample.get('non', 1)}")

    print(f"判断key是否包含：{'name' in dict_sample}")
    print(f"判断value是否包含：{'jason' in dict_sample.values()}")
    print(f"判断key和value是否包含：{[k + ':' + v for k, v in dict_sample.items() if k == 'name' and v == 'jason' ]}")

    # 增加key-value
    dict_sample['gender'] = 'male'
    dict_sample['birthday'] = '2000-01-01'
    print(f"增加键值对：{dict_sample}")

    # 更新键值对
    dict_sample['gender'] = 'female'
    print(f"更新键值对：{dict_sample}")

    # 删除键值对
    dict_sample.pop('birthday')
    print(f"删除键值对：{dict_sample}")

    print(f"根据字典key进行升序排序，返回排序后的键值对列表：{sorted(dict_sample.items(), key=lambda x: x[0])}")
    print(f"根据字典key进行降序排序，返回排序后的键值对列表：{sorted(dict_sample.items(), key=lambda x: x[0], reverse=True)}")

    # 排序时需要确保元素类型一致，如果不一致则会报错：TypeError: '<' not supported between instances of 'int' and 'str'
    print(f"根据字典value进行升序排序，返回排序后的键值对列表：{sorted({'b': 1, 'a': 2, 'c': 10}.items(), key=lambda x: x[1])}")
    print(f"根据字典value进行降序排序，返回排序后的键值对列表：{sorted({'b': 1, 'a': 2, 'c': 10}.items(), key=lambda x: x[1], reverse=True)}")

    print()


# 展示集合初始化的各种方法
def set_example():

    print(f"直接初始化：{set_sample}")

    # noinspection PySetFunctionToLiteral
    print(f"set方法-集合初始化：{set([1, '2', 3.0])}")

    print(f"元素是否在集合内：{1 in set_sample}")

    set_sample.add(5)
    print(f"增加元素：{set_sample}")

    set_sample.remove(5)
    print(f"删除元素：{set_sample}")

    # pop删除的是集合中的最后一个元素，因为集合是无序的，所以无法确认删除的是哪个元素
    set_sample.pop()
    print(f"pop删除元素：{set_sample}")

    print(f"升序排序：{sorted(set_sample)}")
    print(f"降序排序：{sorted(set_sample, reverse=True)}")

    print()


# set/集合：产品的价格去重，返回去重后的元素长度
def find_unique_price_using_set(products):
    unique_price_set = set()
    for _, price in products:
        unique_price_set.add(price)
    return len(unique_price_set)


# list/列表：产品的价格去重，返回去重后的元素长度
def find_unique_price_using_list(products):
    unique_price_list = []
    # A
    for _, price in products:
        # B
        if price not in unique_price_list:
            unique_price_list.append(price)
    return len(unique_price_list)


def benchmark():
    product_id_list = [x for x in range(0, 100000)]
    product_price_list = [x for x in range(200000, 300000)]

    # 使用zip，将product_id和product_price按照索引打包成元组，然后转换成列表
    # zip函数可以将product_id_list和product_price_list按照索引顺序打包成一个个的元组，最终包装成一个zip对象，再通过list函数进行转换
    # 比如[1, 2, 3]和[4, 5, 6, 7]，最终可以打包成[(1, 4), (2, 5), (3, 6)]
    products = list(zip(product_id_list, product_price_list))

    # 计算列表版本的时间
    # 31.58982079999987
    start_using_list = time.perf_counter()
    find_unique_price_using_list(products)
    end_using_list = time.perf_counter()
    print("time elapse using list: {}".format(end_using_list - start_using_list))

    # 计算集合版本的时间
    # 0.008213499968405813
    start_using_set = time.perf_counter()
    find_unique_price_using_set(products)
    end_using_set = time.perf_counter()
    print("time elapse using set: {}".format(end_using_set - start_using_set))

    # 在列表中，要先判断价格是否已在列表中，这个是一个线性的操作，时间复杂度是O(n)，甚至理论上来说，最差可能是，但是在集合中，是个哈希计算操作，时间复杂度是O(1)
    # 整体复杂度则分配是O(n^2)和O(n)


# 基准测试：集合初始化方法更快
def benchmark_think():
    print()

    length = 100000

    dict_list = [dict() for _ in range(length)]

    # 直接花括号new
    # 0.03044719999888912
    start_using_set = time.perf_counter()
    [dict_list.insert(i, {'name': 'jason', 'age': 20, 'gender': 'male'}) for i in range(length)]
    end_using_set = time.perf_counter()
    print("time elapse using new bracket: {}".format(end_using_set - start_using_set))

    # 使用dict函数
    # 0.05973379994975403
    start_using_set = time.perf_counter()
    [dict_list.insert(i, dict({'name': 'jason', 'age': 20, 'gender': 'male'})) for i in range(length)]
    end_using_set = time.perf_counter()
    print("time elapse using dict function: {}".format(end_using_set - start_using_set))

    print()


# 基准测试：集合初始化方法更快
def benchmark_think_timeit():
    print()

    length = 1000
    # 一轮测试要执行多少次代码才算完成
    number = 50
    # repeat参数则代表要执行多少轮测试
    repeat = 10

    setup = 'dict_list = [dict() for _ in range(length)]'
    global_param = {'length': length}
    new_bracket_code = "[dict_list.insert(i, {'name': 'jason', 'age': 20, 'gender': 'male'}) for i in range(length)]"
    dict_func_code = "[dict_list.insert(i, dict({'name': 'jason', 'age': 20, 'gender': 'male'})) " \
                     "for i in range(length)]"

    new_bracket_rtl = timeit.repeat(stmt=new_bracket_code, setup=setup, repeat=repeat, number=number,
                                    globals=global_param)
    dict_func_rtl = timeit.repeat(stmt=dict_func_code, setup=setup, repeat=repeat, number=number, globals=global_param)

    # 相对来说，直接使用花括号的效率会更高一点，但是没有高很多，初始化1000个字典的代码，执行50次，才相差3毫秒左右
    # 平均：431.28885001060553 ms
    print(f"time elapse using new bracket: {statistics.mean(new_bracket_rtl) * 1000} ms")
    # 平均：434.18177999556065 ms
    print(f"time elapse using dict function: {statistics.mean(dict_func_rtl) * 1000} ms")

    print()


def dict_elem_list():
    print(f"字典中key和value是集合的初始化：{{'name': 'jason', ['education']: ['Tsinghua University', 'Stanford University']}}")


if __name__ == '__main__':
    dict_example()
    set_example()
    dict_elem_list()
    # benchmark()
    # benchmark_think()
    benchmark_think_timeit()
