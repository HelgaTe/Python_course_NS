from datetime import datetime


class Parent:
    def __init__(self, name):
        print('Parent __init__')
        self.name = name

    def info(self):
        print(f'parent {self.name}')


class Child(Parent):
    def __init__(self, name,
                 count):  # если метод __init__ есть в дочернем классе, то используется этот __init__, в противном случаии - из родителького класса
        print('Child __init__')
        # self.name=name # если метод родительского класса завязан на переменную, которая определена в __init__, то ее надо инициализировать в дочернем классе, чтобы она была доступна
        # Parent.__init__(self, name) # the line above is re-stated, но тут мы привязаны к конкретному родителю, что может быть неудобно, если у нас большая иерархия
        # super().__init__(name) #1 equal to #2 : ищет __init__ не только в конкретном родительском классе, но в людом родительскои выше (более гибкий вариант)
        super(Child, self).__init__(name)  # 2 equal to 1
        self.count = count

    def date(self):
        print(f'Current time is : {datetime.now()}')


if __name__ == '__main__':
    # c1=Child() # for case <class Child(Parent) // pass> : parent class has __init__ and requires 'name'
    # print(c1) # stdout <TypeError: __init__() missing 1 required positional argument: 'name'>

    # c2=Child('child2') # <click tab >>> the object possess methods inherited from both classes>
    # print(c2.date())

    c3 = Child('child3', 10)  # the case when 'name' is added into __init__ (Child class)
    print(c3.info())
    print(c3.date())
