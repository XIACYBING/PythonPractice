# 类是同一类事物的聚合，比如猫和狗都是动物，直线和圆都是平面几何图形，哈利波特和权利游戏都是文档（小说），它们都有相同的特性，这些特性可以抽象成属性和方法，从而构成类
# 类实例则是一个具体的事物，比如哈利波特是文档类的一个类实例
# 方法：构造器方法、成员方法、类方法、静态方法
# 属性：公共属性、私有属性
# 访问权限：属性或方法（成员方法、类方法和静态方法），如果名称是__开头的，说明是私有的，都只能在类中访问
# class/类以class关键字标识，结构如下：
from abc import ABCMeta, abstractmethod


class Document:

    # 如果某个类有一些常量，则可以直接在类中定义，这样就可以不用每次都在类实例中声明
    DOCUMENT_STR = "DOCUMENT"

    __PRIVATE_DOCUMENT = "PRIVATE_DOCUMENT"

    def __init__(self, author, title, context):
        # 和Java不同，Python类的属性，在init构造器中用self声明即可，不需要额外在类中声明
        self.author = author
        self.title = title
        # 属性命名以__作为前缀的，代表是个私有属性，外部无法直接访问，只能类实例内部访问，或者通过某些类方法间接被外部访问（类似Java中的getter/setter方法）
        self.__context = context
    
    # 类的成员方法中第一个参数必须是self，如果使用类实例进行调用，默认就是对应的类实例
    # 如果直接用Document.get_context_len()，则参数必须传入一个Document类实例
    # 其实Java中也有类似的机制，每个类方法中第一个参数是类实例本身，参数名是this
    def get_context_len(self) -> int:
        return len(self.__context)

    # 成员方法的参数和返回值都是可选的，但是需要注意，参数如果要用，一定要声明，返回值如果声明了，一定要有，如果没声明，可以有也可以没有
    def get_context(self):
        return self.__context

    # 如果一个方法用@staticmethod，说明这是个静态方法，外部可以在没有类实例的时候直接调用，当然，也可以由类实例发起调用
    # 可以发现，相比于成员方法和self，类方法的cls，静态方法其实和类没啥直接关联，可以将和类没有直接关联的行为的表现为静态方法
    @staticmethod
    def access_private_constant():
        print(f"私有常量只能在类实例中被访问：{Document.__PRIVATE_DOCUMENT}")

    # 类方法用@classmethod主机额装饰，类方法是直接绑定到类上，第一个参数cls代表类本身，比如当前场景，cls可以等价为Document
    # 类方法可以由类或者类实例访问，和静态方法不同的是，类方法会包含类信息（也就是cls），适用于
    @classmethod
    def create_harry_potter_doc(cls, title, context):
        return cls('J.K.Rowling', title, context)

    @classmethod
    def print_class_name(cls):
        print(f"当前类是：{cls.__name__}")


twelve_context = Document('', '', 'i am context')
seventeen_context = Document('', '', 'i am second context')

print(f"公共常量可以被外部直接访问：{Document.DOCUMENT_STR}")
Document.access_private_constant()

print()
# 其实类访问成员方法也得有一个类实例，所以可以说成员方法需要类实例才能访问，但是类方法和静态方法可以被类或类实例发起访问
print(f"类实例直接访问方法：{twelve_context.get_context_len()}")
print(f"类访问方法：{Document.get_context_len(seventeen_context)}")

print()
print("静态方法访问示例：")
# 静态方法可以由类访问，也可以由类实例来访问
Document.access_private_constant()
twelve_context.access_private_constant()

print()
# 类方法也可以由类/类实例访问
Document.print_class_name()
twelve_context.print_class_name()


# 类是一群相似对象的集合，而父类就是一群相似类的集合
# 比如我有一个Entity类，代表所有实体，而Video/Music，就是实体之一
class Entity:
    def __init__(self, obj_type):
        self.obj_type = obj_type

    # 父类可以定义一些方法，这些方法需要由子类来实现，不然无法调用
    def get_context_len(self):
        raise Exception('get_context_len not implemented')

    # 父类还可以定义一些子类共有的方法，比如下面这个get_title，由title属性的子类可以直接调用，没有title属性的子类调用会报错
    # 这点和Java很不一样，在Java中，父类没有定义的属性，一定不能使用，在Python中，却可以“提前”使用
    # 但是从我个人角度出发，我更倾向于在Entity下再定义一个TitleEntity类，然后在该类中定义get_title方法，代码可读性更高，结构也更明确
    # noinspection PyUnresolvedReferences
    def get_title(self) -> str:
        return self.title


# 在子类中，如果想要正确的初始化父类，需要显式调用父类的init方法，方式有多种多样：
# 1、使用super().__init__(...)，这个方法比较推荐，因为简洁且能动态解析，且在多继承的情况下比较友好 todo 学习动态解析、多继承mro的知识
# 2、使用Parent.__init__(...)，Parent代表具体的父类名称，比如Music类的父类是Entity，这种方式的指向性强且直观，但是不适用于多继承  todo 确认为什么不适用于多继承
# 3、使用super(Child, self).__init__(...)，这是Python2遗留下来的兼容方式，能精准控制MRO，但是因为冗长而不推荐   todo 学习MRO，确认为什么能精准控制MRO
# 4、分别调用父类的init函数，这是在多继承的情况下可以这么做，能够精确控制每个父类的初始化，但是复杂继承场景可能导致重复或者遗漏初始化
# 除此之外，不调用父类init函数其实也是可行的，但是不推荐，因为可能导致父类的某些状态没有正常初始化，只有在明确不需要初始化父类的时候才可以这么做。
class Music(Entity):
    def __init__(self, name, time, content):
        Entity.__init__(self, 'music')
        self.name = name
        self.time = time
        self.__content = content


class Video(Entity):
    def __init__(self, name, time, content):
        super().__init__('video')
        self.name = name
        self.time = time
        self.__content = content


# 除了普通类外，还有一种抽象类，和Java的抽象类类似，定义一些父类共有方法
# 抽象类必须继承ABCMeta，此外，抽象类下的抽象方法必须用@abstractmethod标记
# 抽象类生来就是父类，无法直接实例化，必须由某个子类继承实现后才能实例化，这一点和Java一样
# todo 确认python中是否有接口存在，以及确认python和Java中类、抽象类和抽象方法等的对比
class TitleEntity(metaclass=ABCMeta, Entity):

    def __init__(self, obj_type, title):
        super(TitleEntity, self).__init__(obj_type)
        self.title = title

    # 此处演示方法重写，以及从我自己角度出发，我更倾向于将get_title定义在这一层级
    def get_title(self) -> str:
        return self.title

    # 抽象方法，子类必须要实现
    @abstractmethod
    def modify_title(self, title):
        pass


class TitleNovel(TitleEntity):
    def __init__(self, title, author, context):
        super().__init__('novel', title)
        self.author = author
        self.__context = context

    # 实现抽象方法
    def modify_title(self, title):
        super().title = title

# todo 确认多重继承、菱形继承中，构造器实现的顺序是怎么样的


if __name__ == '__main__':
    pass
