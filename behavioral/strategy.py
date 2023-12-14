def default_meow_strategy():
    print("Meow")


def angry_meow_strategy():
    print("MEOWWWWWWWWWWWWWWWWWW!!!!!!!!!!!!!")


def hungry_meow_strategy():
    print("Meowww!!! Meoowww meowwwwwwww meeow")


def default_jump_strategy():
    print("Simple jump")


def big_jump_strategy():
    print("BIG JUMP BAX BUX")


class Cat:
    def __init__(
        self, meow_strategy=default_meow_strategy, jump_strategy=default_jump_strategy
    ):
        self.meow_strategy = meow_strategy
        self.jump_strategy = jump_strategy

    def meow(self):
        self.meow_strategy()

    def jump(self):
        self.jump_strategy()


c1: Cat = Cat()
c1.meow()
c1.jump()

print()
c2: Cat = Cat(meow_strategy=angry_meow_strategy)
c2.meow()
c2.jump()

print()
c3: Cat = Cat(meow_strategy=hungry_meow_strategy)
c3.meow()
c3.jump()

print()
c4: Cat = Cat(meow_strategy=angry_meow_strategy, jump_strategy=big_jump_strategy)
c4.meow()
c4.jump()
