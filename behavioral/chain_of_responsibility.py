from abc import ABC, abstractmethod
from collections import namedtuple
from math import sqrt

NumberEvent = namedtuple("NumberEvent", "type value")


class Handler(ABC):
    @abstractmethod
    def set_next(self, handler: "Handler") -> "Handler":
        pass

    @abstractmethod
    def handle(self, data: NumberEvent) -> int:
        pass


class AbstractHandler(Handler):
    _next_handler: Handler = None

    def __init__(self, next_handler: "AbstractHandler" = None):
        if next_handler:
            self.set_next(next_handler)

    def set_next(self, handler: "Handler") -> "Handler":
        self._next_handler = handler
        return handler

    def handle(self, data: NumberEvent) -> int:
        if self._next_handler:
            return self._next_handler.handle(data)
        return 0


class IdentityHandler(AbstractHandler):
    def handle(self, data: NumberEvent) -> int:
        if data.type == "identity":
            return data.value
        return super().handle(data)


class SquareHandler(AbstractHandler):
    def handle(self, data: NumberEvent) -> int:
        if data.type == "square":
            return data.value * data.value
        return super().handle(data)


class SqrtHandler(AbstractHandler):
    def handle(self, data: NumberEvent) -> int:
        if data.type == "sqrt":
            return int(sqrt(data.value))
        return super().handle(data)


def create_handler() -> AbstractHandler:
    h1: AbstractHandler = IdentityHandler()
    h2: AbstractHandler = SqrtHandler()
    h3: AbstractHandler = SquareHandler()
    h1.set_next(h2)
    h2.set_next(h3)
    return h1


def test_identity_handler():
    handler: AbstractHandler = create_handler()
    event: NumberEvent = NumberEvent("identity", 2)
    assert handler.handle(event) == 2


def test_square_handler():
    handler: AbstractHandler = create_handler()
    event: NumberEvent = NumberEvent("square", 2)
    assert handler.handle(event) == 4


def test_sqrt_handler():
    handler: AbstractHandler = create_handler()
    event: NumberEvent = NumberEvent("sqrt", 25)
    assert handler.handle(event) == 5


def test_wrong_handler():
    handler: AbstractHandler = create_handler()
    event: NumberEvent = NumberEvent("random_here", 100)
    assert handler.handle(event) == 0


def test_constructor_handling():
    handler: AbstractHandler = IdentityHandler(SquareHandler(SqrtHandler()))
    square_event: NumberEvent = NumberEvent("square", 7)
    identity_event: NumberEvent = NumberEvent("identity", 9)
    invalid_event: NumberEvent = NumberEvent("invalid", 10)
    assert handler.handle(square_event) == 49
    assert handler.handle(identity_event) == 9
    assert handler.handle(invalid_event) == 0
