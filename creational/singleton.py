class Singleton:
    _instance: "Singleton" = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance


def test_singleton():
    s1: Singleton = Singleton()
    s2: Singleton = Singleton()
    assert s1 is s2


# Other way to implement singleton in python using metaclasses
class SingletonMetaclass(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class Singleton2(metaclass=SingletonMetaclass):
    pass


def test_singleton_with_metaclass():
    s1: Singleton2 = Singleton2()
    s2: Singleton2 = Singleton2()
    assert s1 is s2