from abc import ABC, abstractmethod
import random
from typing import List


class CoinBox(ABC):

    @abstractmethod
    def unpack(self) -> int:
        pass


class FixedValueCoinBox(CoinBox):

    def __init__(self, value: int) -> None:
        self._value = value

    def unpack(self) -> int:
        return self._value


class LuckyCoinBox(CoinBox):

    def unpack(self) -> int:
        return random.randint(1, 100)


class MultipleCoinBox(CoinBox):
    def __init__(self) -> None:
        self._boxes: List[CoinBox] = []

    def add_box(self, box: CoinBox) -> None:
        self._boxes.append(box)

    def unpack(self) -> int:
        return sum([box.unpack() for box in self._boxes])


box1: FixedValueCoinBox = FixedValueCoinBox(25)
print("Value box: ", box1.unpack())

box2: LuckyCoinBox = LuckyCoinBox()
print("Lucky box: ", box2.unpack())

box3: MultipleCoinBox = MultipleCoinBox()
box3.add_box(box1)
box3.add_box(box2)
print("Multiple box: ", box3.unpack())

box4: MultipleCoinBox = MultipleCoinBox()
box4.add_box(box1)
box4.add_box(box3)
print("Multiple Multiple box: ", box4.unpack())

