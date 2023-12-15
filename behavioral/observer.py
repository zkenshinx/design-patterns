from typing import List, Any
from abc import ABC, abstractmethod


class Subject(ABC):

    @abstractmethod
    def subscribe(self, observer: "Observer") -> None:
        pass

    @abstractmethod
    def unsubscribe(self, observer: "Observer") -> None:
        pass

    @abstractmethod
    def notify(self) -> None:
        pass


class ChatRoom(Subject):
    observers: List["Observer"] = []
    current_user: str
    current_message: str

    def subscribe(self, observer: "Observer") -> None:
        if observer not in self.observers:
            self.observers.append(observer)

    def unsubscribe(self, observer: "Observer") -> None:
        if observer in self.observers:
            self.observers.remove(observer)

    def notify(self) -> None:
        for observer in self.observers:
            message_event = (self.current_user, self.current_message)
            observer.update(message_event)

    # Some business logic
    def send_message(self, user: str, message: str) -> None:
        self.current_user: str = user
        self.current_message: str = message
        self.notify()


class Observer(ABC):
    def update(self, event: Any) -> None:
        pass


class User(Observer):
    username: str
    chatroom: ChatRoom

    def __init__(self, username: str) -> None:
        self.username = username

    def join_chatroom(self, chatroom: ChatRoom) -> None:
        self.chatroom = chatroom

    def update(self, event) -> None:
        other_user, message = event
        if other_user != self.username:
            print("{} got message from {}: '{}'".format(self.username, other_user, message))

    def send_message(self, message: str) -> None:
        self.chatroom.send_message(self.username, message)


class ChatRoomLogger(Observer):
    def update(self, event) -> None:
        user, message = event
        print("Log: user '{}' send message: '{}' to chat room".format(user, message))


chatroom = ChatRoom()
user1 = User("kenrick")
user2 = User("zken")
user3 = User("kaneki")

user1.join_chatroom(chatroom)
chatroom.subscribe(user1)

user2.join_chatroom(chatroom)
chatroom.subscribe(user2)

user3.join_chatroom(chatroom)
chatroom.subscribe(user3)

logger = ChatRoomLogger()
chatroom.subscribe(logger)

user1.send_message("Hey guys, How are you?")

print()
user2.send_message("Hey fine, what about you?")
