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
        user = UserService().get_current_user().model_dump()
        output = f"Current User: {user.username}\nEmail: {user.email}"
        return output

    def help(self):
        """
        Display help information for the whoami command.
        """
        return "Use this command to display the current user's information."