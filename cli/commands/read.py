from cli.command import Command
from services.file_service import FileService


class ReadCommand(Command):
    """
    Command to read the content a file.
    This command is used to read the contents of a specified file.
    """

    def execute(self, args):
        """
        Execute the read command.
        
        :param file_path: Name of the file to read.
        """
        if not args or not isinstance(args[0], str) or not args[0].strip():
            raise ValueError("File name must be provided and cannot be empty.")
        
        file_path = args[0]
        print(FileService().read_file(file_path))
        return True

    def help(self):
        """
        Display help information for the read command.
        """
        print(FileService().help())