from cli.command import Command
from services.file_service import FileService
from services.user_service import UserService


class MetadataCommand(Command):
    """
    Command to read metadata.
    This command is used to read the metadata of a specified file.
    """

    def execute(self, args):
        """
        Execute the metadata command.

        :param file_path: Name of the file to read metadata.
        """
        if not args or not isinstance(args[0], str) or not args[0].strip():
            raise ValueError("File name must be provided and cannot be empty.")

        file_path = args[0]
        metadata = FileService().read_metadata(file_path)
        if metadata:
            print(f"\nMetadata for {file_path}:\n")
            print(f"File Name: {metadata.get('file_name', None)}\nFile ID: {metadata.get('file_id', None)}\nFile Size: {metadata.get('file_size', None)}\nFile Path: {metadata.get("file_path", None)}\nVisibility: {metadata.get("visibility", None)}\nCreated At: {metadata.get('created_at', None)}\n")

        else:
            print(f"No metadata found for {file_path}.")
        return True

    def help(self):
        """
        Display help information for the metadata command.
        """
        return FileService().help()