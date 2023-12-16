from abc import ABC, abstractmethod


# Adaptee
class LegacyConsoleWriter:

    def write(self, message: str) -> None:
        print(message)


# Target Interface
class Printer(ABC):

    @abstractmethod
    def print(self, message: str) -> None:
        pass


# Adapter
class ConsolePrinter(Printer):
    legacy_writer: LegacyConsoleWriter = LegacyConsoleWriter()

    def print(self, message: str) -> None:
        self.legacy_writer.write(message)


printer: ConsolePrinter = ConsolePrinter()
printer.print("Hello World")
