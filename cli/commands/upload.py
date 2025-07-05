from cli.command import Command
from services.file_service import FileService
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
        file_path = args[0] if args else None

        if not file_path:
            raise ValueError("File path must be provided.")
        if not isinstance(file_path, str):
            raise ValueError("File path must be a string.")
        if not file_path.strip():
            raise ValueError("File path cannot be empty or whitespace.")
        if not os.path.isfile(file_path):
            raise ValueError(f"File does not exist: {file_path}")
        
        return FileService().upload_file(file_path)

    def help(self):
        """
        Display help information for the upload command.
        """
        print(FileService().help())