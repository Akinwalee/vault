from cli.command import Command
from services.file_service import FileService


class LsCommand(Command):
    """
    List all files in a given directory.
    """
    
    def execute(self, args):
        
        directory_name = args[0] if args else 'root'
        if directory_name:
            directory = FileService().get_directory(directory_name=directory_name)
            if not directory:
                raise ValueError("Directory '{directory_name}' does not exist.")
    
        metadata = FileService().get_folder_files(directory_name)
        if not metadata:
            return "No files found in the specified directory."
        
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
        return "List all files in a given directory."