

class A:
    def __init__(self):
        self.b_class = B(some_value=1)

class B:
    def __init__(self, **kwargs):
        self.variable = kwargs.get("some_value")
        print(self.variable)

class C:
    def  __init__(self):
        self.b_class_one_more = B()
        print('123')

j = A()
z = C()