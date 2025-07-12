from cli.cli import click
from services.user_service import UserService
from cli.command import Command


class LoginCommand(Command):
    """
    Command to log in a user.
    This command is used to authenticate a user and create a session.
    """

    def execute(self, args):
        """
        Execute the login command.
        
        :param username: Username of the user.
        :param password: Password of the user.
        """
        username = click.prompt('Enter your username', type=str)
        password = click.prompt('Enter your password', type=str, hide_input=True)
        args = (username, password)
        if len(args) != 2:
            raise ValueError("Username and password must be provided.")
        
        if not username or not password:
            raise ValueError("Username and password cannot be empty.")
        
        return UserService().login_user(username, password)

    def help(self):
        """
        Display help information for the login command.
        """
        return "Use this command to log in with your username and password."