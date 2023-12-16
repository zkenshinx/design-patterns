from abc import ABC, abstractmethod


class PlayerState(ABC):
    _player: "Player" = None

    def __init__(self, player: "Player" = None) -> None:
        self._player = player

    @property
    def player(self) -> "Player":
        return self._player

    @player.setter
    def player(self, player: "Player"):
        self._player = player

    @abstractmethod
    def take_potion(self, potion: str) -> None:
        pass

    @abstractmethod
    def heal(self, heal_amount: int) -> None:
        pass

    @abstractmethod
    def take_damage(self, damage: int) -> None:
        pass


class PlayerAliveState(PlayerState):

    def take_potion(self, potion: str):
        pass

    def heal(self, heal_amount: int):
        self.player.health = min(self.player.health + heal_amount, 100)

    def take_damage(self, damage: int) -> None:
        self.player.health = max(self.player.health - damage, 0)
        if self.player.health <= 0:
            self.player.player_state = PlayerDeadState(player=self.player)
        elif self.player.health <= 30:
            self.player.player_state = PlayerInjuredState(player=self.player)


class PlayerDeadState(PlayerState):

    def take_potion(self, potion: str) -> None:
        if potion == "zombify":
            self.player.health = 100
            self.player.player_state = PlayerZombieState(player=self.player)

    def heal(self, heal_amount: int):
        pass

    def take_damage(self, damage: int) -> None:
        pass


class PlayerZombieState(PlayerState):

    def take_potion(self, potion: str) -> None:
        if potion == "cure":
            self.player.health = 20
            self.player.player_state = PlayerInjuredState(player=self.player)

    def heal(self, heal_amount: int):
        self.player.health = min(self.player.health + int(1.5 * heal_amount), 100)

    def take_damage(self, damage: int) -> None:
        self.player.health -= int(0.8 * damage)
        if self.player.health <= 0:
            self.player.health = 0
            self.player.player_state = PlayerDeadState(player=self.player)


class PlayerInjuredState(PlayerState):

    def take_potion(self, potion: str) -> None:
        pass

    def heal(self, heal_amount: int):
        self.player.health = min(self.player.health + int(0.9 * heal_amount), 100)

    def take_damage(self, damage: int) -> None:
        self.player.health -= int(1.1 * damage)
        if self.player.health <= 0:
            self.player.health = 0
            self.player.player_state = PlayerDeadState(player=self.player)


class Player:
    player_state: PlayerState
    health: int

    def __init__(self, player_state: PlayerState, health: int = 100) -> None:
        self.player_state = player_state
        self.player_state.player = self
        self.health = health

    def take_potion(self, potion: str) -> None:
        self.player_state.take_potion(potion)

    def heal(self, heal_amount: int):
        self.player_state.heal(heal_amount)

    def take_damage(self, damage: int) -> None:
        self.player_state.take_damage(damage)

    # Some other logic for player


def test_damaging_alive_to_injured_state() -> None:
    player = Player(player_state=PlayerAliveState())
    player.take_damage(80)
    assert type(player.player_state).__name__ == 'PlayerInjuredState'


def test_damaging_alive_with_its_whole_health() -> None:
    player = Player(player_state=PlayerAliveState())
    player.take_damage(100)
    assert type(player.player_state).__name__ == 'PlayerDeadState'


def test_damaging_alive_with_more_than_its_health() -> None:
    player = Player(player_state=PlayerAliveState())
    player.take_damage(150)
    assert type(player.player_state).__name__ == 'PlayerDeadState'


def test_damaging_alive_with_small_damage() -> None:
    player = Player(player_state=PlayerAliveState())
    player.take_damage(5)
    assert type(player.player_state).__name__ == 'PlayerAliveState'


def test_damaging_injured_to_death() -> None:
    player = Player(player_state=PlayerInjuredState())
    player.health = 15
    player.take_damage(20)
    assert type(player.player_state).__name__ == 'PlayerDeadState'


def test_dead_remains_dead() -> None:
    player = Player(player_state=PlayerDeadState())
    player.take_damage(1)
    assert type(player.player_state).__name__ == 'PlayerDeadState'


def test_dead_becomes_zombie_with_zombify() -> None:
    player = Player(player_state=PlayerDeadState())
    player.take_potion("zombify")
    assert type(player.player_state).__name__ == 'PlayerZombieState'


def test_zombie_gets_cured_with_cure_and_becomes_injured() -> None:
    player = Player(player_state=PlayerZombieState())
    player.take_potion("cure")
    assert type(player.player_state).__name__ == 'PlayerInjuredState'
