from cli.command import Command
from services.file_service import FileService
from services.user_service import UserService
import os


class UploadCommand(Command):
    """
    Command to upload a file.
    This command is used to upload files to the server.
    """

    def execute(self, args):
        """
        Execute the upload command.
        
        :param file_path: Path to the file to upload.
        """
        user_id = UserService.get_user_id()
        if not user_id:
            raise ValueError("No user session found. Cannot upload file.")
        if len(args) > 2:
            raise ValueError("Usage: vault upload <file_name> <directory_name>")

        file_path = args[0] if args else None
        directory_name = args[1] if len(args) > 1 else 'root'

        if not file_path:
            raise ValueError("File path must be provided.")
        if not isinstance(file_path, str):
            raise ValueError("File path must be a string.")
        if not file_path.strip():
            raise ValueError("File path cannot be empty or whitespace.")
        if not os.path.isfile(file_path):
            raise ValueError(f"File does not exist: {file_path}")

        file_name = file_path.split('/')[-1]
        with open(file_path, 'rb') as f:
            data = f.read()

        return FileService().upload_file(file_name, data, directory_name=directory_name, user_id=user_id)

    def help(self):
        """
        Display help information for the upload command.
        """
        return FileService().help()
