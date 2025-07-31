from cli.command import Command
from services.file_service import FileService

class ListCommand(Command):
    """
    Command to list files.
    This command is used to list files in the specified directory.
    """

    def execute(self, args):
        """
        Execute the list command.
        :param args: Additional arguments (not used).
        """

        
        metadata = FileService().list_files()
        if not metadata:
            return ("No files found.")
        if metadata:
            table = f"{'ID':<24}| {'File Name':<12}| {'Size (bytes)':<9}| {'Uploaded At':<20} \n{'-'*24}| {'-'*12}| {'-'*12}| {'-'*20}"
    
            for key, data in metadata.items():
                file_name = data.get("file_name", "Unknown")
                file_size = data.get("file_size", "Unknown")
                created_at = data.get("created_at", "Unknown")
                id = data.get("file_id", "Unknown")
                file_row = f"{id:<20}| {file_name:<12}| {file_size:<12}| {created_at:<20}"
                table += f"\n{file_row}"
        return (f'\n{table}')

    def help(self):
        """
        Display help information for the list command.
        """
        return FileService().help()
