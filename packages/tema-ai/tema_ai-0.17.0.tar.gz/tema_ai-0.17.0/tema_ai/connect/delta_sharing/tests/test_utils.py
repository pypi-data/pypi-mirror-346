from ..utils import Singleton

VALUE = 10


@Singleton
class singleton:
    def __init__(self):
        self.a = VALUE

    def update(self, a):
        self.a = a


class NoSingleton:
    def __init__(self):
        self.a = VALUE

    def update(self, a):
        self.a = a


class TestSingleton:
    def test(self):
        # two instances should reference the same
        inst1 = singleton.instance()
        inst2 = singleton.instance()
        # same memory address
        assert id(inst1) == id(inst2)
        assert inst1.a == VALUE and inst2.a == VALUE

        # We update instance 1 at it affects isntance 2
        inst1.update(20)
        assert inst1.a == 20 and inst2.a == 20

    def test_no_singleton(self):
        # two instances should reference the same
        inst1 = NoSingleton()
        inst2 = NoSingleton()
        # same memory address
        assert id(inst1) != id(inst2)
        assert inst1.a == VALUE and inst2.a == VALUE

        # We update instance 1 at it affects isntance 2
        inst1.update(20)
        assert inst1.a == 20 and inst2.a != 20
