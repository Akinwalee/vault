from cli.command import Command
from services.user_service import UserService


class LogoutCommand(Command):
    """
    Command to log out a user.
    This command is used to terminate the user's session.
    """

    def execute(self, args):
        """
        Execute the logout command.
        
        :param args: Additional arguments (not used).
        """
        return UserService().logout_user()

    def help(self):
        """
        Display help information for the logout command.
        """
        return "Use this command to log out of your account."
