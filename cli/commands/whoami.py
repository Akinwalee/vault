from cli.command import Command
from services.user_service import UserService


class WhoamiCommand(Command):
    """
    Command to display the current user's information.
    This command is used to retrieve the details of the logged-in user.
    """

    def execute(self, args):
        """
        Execute the whoami command.
        
        :param args: Additional arguments (not used).
        """
        current_user = UserService().get_current_user()
        if not current_user:
            raise ValueError("No user session found.")

        output = f"\nCurrent User: {current_user.username}\nEmail: {current_user.email}"
        return output

    def help(self):
        """
        Display help information for the whoami command.
        """
        return "Use this command to display the current user's information."