from cli.commands.test import TestCommand
from cli.commands.upload import UploadCommand
from cli.commands.list import ListCommand
from cli.commands.read import ReadCommand
from cli.commands.metadata import MetadataCommand
from cli.commands.delete import DeleteCommand
from cli.commands.register import RegisterCommand
from cli.commands.login import LoginCommand
from cli.commands.logout import LogoutCommand
from cli.commands.whoami import WhoamiCommand
from cli.commands.publish import PublishCommand
from cli.commands.unpublish import UnpublishCommand


COMMANDS = {
    "test": TestCommand,
    "upload": UploadCommand,
    "list": ListCommand,
    "read": ReadCommand,
    "metadata": MetadataCommand,
    "delete": DeleteCommand,
    "register": RegisterCommand,
    "login": LoginCommand,
    "logout": LogoutCommand,
    "whoami": WhoamiCommand,
    "publish": PublishCommand,
    "unpublish": UnpublishCommand
}

def route_command(command_name, *args):
    """
    Route the command to the appropriate command class.
    
    :param command_name: The name of the command to execute.
    :param args: Positional arguments for the command.
    :return: The result of the command execution.
    """
    command_class = COMMANDS.get(command_name)
    if not command_class:
        raise ValueError(f"Command '{command_name}' not found.")
    
    if args and args[0] == "help":
        return command_class().help()

    command_instance = command_class()
    return command_instance.execute(args)