from cli.command import Command
from services.file_service import FileService


class DeleteCommand(Command):
    """
    Command to delete a file.
    This command is used to delete a specified file from the server.
    """

    def execute(self, args):
        """
        Execute the delete command.

        :param file_path: Path to the file to delete.
        """
        if not args or not isinstance(args[0], str) or not args[0].strip():
            raise ValueError("File path must be provided and cannot be empty.")
        
        file_path = args[0]
        return FileService().delete_file(file_path)

    def help(self):
        """
        Display help information for the delete command.
        """
        print(FileService().help())