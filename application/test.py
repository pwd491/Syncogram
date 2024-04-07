from dataclasses import dataclass


@dataclass
class A:
    name: str
    age: int
    @staticmethod
    def example():
        print("Name:")

a = A("Sergey", 22)
print(a.age)