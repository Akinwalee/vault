from cli.command import Command
from services.file_service import FileService


class PublishCommand(Command):
    """
    Command to publish a file.
    This command is used to add the public visibility of a specified file.
    """

    def execute(self, args):
        """
        Execute the unpublish command.
        
        :param file_path: Name of the file to unpublish.
        """
        if not args or not isinstance(args[0], str) or not args[0].strip():
            raise ValueError("File name must be provided and cannot be empty.")
        
        file_name = args[0]
        result = FileService().publish_file(file_name)
        if isinstance(result, dict):
            return f"File '{file_name}' published successfully."
        else:
            raise ValueError(f"Error publishing file '{file_name}': {result}")

    def help(self):
        """
        Display help information for the unpublish command.
        """
        return FileService().help()