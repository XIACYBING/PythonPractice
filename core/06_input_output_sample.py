import json
import os.path


# 简单的输入交互方法
def simple_input():
    print()

    # input方法返回的类型永远是字符串，如果需要其他类型，则要进行类型转换（比如需要数字，用int()或者float()进行转换）
    # input方法会在回车后返回
    name = input('your name:')
    gender = input('you are a boy?(y/n)')

    welcome_str = 'Welcome to the matrix {prefix} {name}.'
    welcome_dic = {
        'prefix': 'Mr.' if gender == 'y' else 'Mrs',
        'name': name
    }

    print('authorizing...')
    print(welcome_str.format(**welcome_dic))


# 对于指定的文件，读取所有行，按照空格切割后进行字符的统计
def read_statistics():

    word_count_dict = {}

    # read()方法一次性返回文件中所有字符
    # readline()每次返回一行，最后一次返回空
    # readlines()会以列表的方式返回所有的行
    # readline(int)和read(int)会读取指定字符，比如第一行是abcd，第二行是efgh，readline(2)每次调用的返回如下：ab,cd, e,fg,h
    # for line in file，会将file作为一个迭代器，将每行字符作为元素进行迭代
    with open(file='05_string_sample.py', mode='r', encoding='UTF-8') as file:
        for line in file:
            line = line.strip()
            if len(line) == 0 or '# ' in line:
                continue

            # 按照空格切割，然后放入dict中
            for word in line.split(' '):
                if word in word_count_dict:
                    word_count_dict[word] = word_count_dict[word] + 1
                else:
                    word_count_dict[word] = 1

        # 按照值倒序排序
        word_count_dict = sorted(word_count_dict.items(), key=lambda x: x[1], reverse=True)
        [print(f"字符：{key}, 出现次数：{value}") for key, value in word_count_dict if value > 3]


# json的demo
def json_def():
    dict_sample = {1: 2, 3: 4}
    dict_str = json.dumps(dict_sample)
    print(f"输出JSON字符串：{dict_str}")
    print(f"重新加载为字典：{json.loads(dict_str)}")

    file_path = 'sample.json'

    # 将json字符串写入文件中
    with open(file=file_path, mode='w', encoding='UTF-8') as file_output:
        json.dump(dict_sample, file_output)

    # 判断文件是否存在
    print(f"文件写入成功：{os.path.exists(file_path)}")

    # 读取文件
    with open(file=file_path, mode='r', encoding='UTF-8') as file_input:
        print(f"加载JSON：{json.load(file_input)}")

    # 删除文件（或者可以用tempFile创建一个临时文件，程序结束了会自动删除）
    os.remove(file_path)
    print(f"删除文件成功：{not os.path.exists(file_path)}")


if __name__ == '__main__':
    # simple_input()
    # read_statistics()
    json_def()
