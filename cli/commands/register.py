from cli.command import Command
from cli.cli import click
from services.user_service import UserService
from storage.models import UserModel
from utils.helpers import get_current_time


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
        args = {'username': username, 'email': email, 'password': password, 'created_at': get_current_time()}
        if not args or len(args) < 3 or not all([args]):
            raise ValueError("Username, email, and password must be provided.")
        
        user = UserModel(**args)
        
        result = UserService.create_user(user)
        if isinstance(user, UserModel):
            return f"User '{result.username}' registered successfully."
        else:
            raise ValueError(f'Error registering user: {result}')
    
    def help(self):
        return super().help()