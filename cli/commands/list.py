from cli.command import Command
from services.file_service import FileService

class ListCommand(Command):
    """
    Command to list files.
    This command is used to list files in the specified directory.
    """

    def execute(self, *args):
        """
        Execute the list command.
        """
        print(FileService().list_files())
        return True

    def help(self):
        """
        Display help information for the list command.
        """
        return FileService().help()