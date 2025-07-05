from abc import ABC, abstractmethod

class Command(ABC):
    """
    Abstract base class for all commands.
    Provides a common interface for command operations.
    """

    @abstractmethod
    def execute(self, *args):
        """
        Execute the command with the given arguments.
        """
        pass

    @abstractmethod
    def help(self):
        """
        Display help information for the command.
        """
        pass