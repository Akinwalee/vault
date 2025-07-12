from cli.command import Command
from services.file_service import FileService
from services.user_service import UserService

class ListCommand(Command):
    """
    Command to list files.
    This command is used to list files in the specified directory.
    """

    def execute(self, *args):
        """
        Execute the list command.
        """
        user = UserService.get_user_id()
        if not user:
            raise ValueError("No user session found. Cannot list files.")
        
        metadata = FileService().list_files()
        if metadata:
            table = f"""
                    {'ID':<36}| {'File Name':<12}| {'Size (bytes)':<9}| {'Uploaded At':<20} \n
                    {'-'*36}| {'-'*12}| {'-'*9}| {'-'*20}"""
    
            for key, data in metadata.items():
                file_name = key
                file_size = data.get("file_size", "Unknown")
                created_at = data.get("created_at", "Unknown")
                id = data.get("id", "Unknown")
                file_row = f"{id:<36}| {file_name:<12}| {file_size:<9}| {created_at:<20}"
                table += f"\n{file_row}"
            print(table)
        return True

    def help(self):
        """
        Display help information for the list command.
        """
        return FileService().help()
