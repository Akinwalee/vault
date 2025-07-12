from cli.command import Command
from services.file_service import FileService
from services.user_service import UserService


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
        
        user = UserService.get_user_id()
        if not user:
            raise ValueError("No user session found. Cannot delete file.")

        file_path = args[0]
        return FileService().delete_file(file_path)

    def help(self):
        """
        Display help information for the delete command.
        """
        return FileService().help()