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
        user = UserService.get_user_id()
        if not user:
            raise ValueError("No user session found. Cannot upload file.")

        file_path = args[0] if args else None

        if not file_path:
            raise ValueError("File path must be provided.")
        if not isinstance(file_path, str):
            raise ValueError("File path must be a string.")
        if not file_path.strip():
            raise ValueError("File path cannot be empty or whitespace.")
        if not os.path.isfile(file_path):
            raise ValueError(f"File does not exist: {file_path}")
        
        return FileService().upload_file(file_path, user_id=user)

    def help(self):
        """
        Display help information for the upload command.
        """
        return FileService().help()
    



    """
    Session.

    redis = {
        "session": {
            "token": "mytoken,
            "user_id": "myuserid",
            }
    }


    session = redis.get("session)
    if session:
        user = session.user_id
    """
