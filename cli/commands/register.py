from cli.command import Command
from cli.cli import click
from services.user_service import UserService
from storage.models import UserModel


class RegisterCommand(Command):
    """
    Command to register a new user.
    This command is used to create a new user account.
    """
    def execute(self, args):
        """
        Execute the register command.
        
        :param user_data: Dictionary containing user information.
        """
        username = click.prompt('Enter your username', type=str)
        email = click.prompt('Enter your email', type=str)
        password = click.prompt('Enter your password', type=str, hide_input=True)
        args = tuple({'username': username, 'email': email, 'password': password}.items())
        if not args or len(args) or not all([args])< 3:
            raise ValueError("Username, email, and password must be provided.")
        
        user = UserModel(**args)
        
        return UserService().create_user(user)