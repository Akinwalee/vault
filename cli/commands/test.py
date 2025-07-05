from cli.command import Command
from services.test_service import TestService

class TestCommand(Command):
    """
    Command to run tests.
    This command is used to execute the test suite.
    """

    def execute(self, *args):
        """
        Execute the test command.
        """
        # Validation ...
        TestService().run_test()

    def help(self):
        """
        Display help information for the test command.
        """
        return TestService().help()