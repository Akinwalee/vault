from cli.command import Command
from services.file_service import FileService


class MkdirCommand(Command):
    """
    Command to create a directory.
    """

    def help(self):
        return "Create a new directory."
    
    def execute(self, *args):
        if len(args) < 1:
            return "Usage: mkdir <directory_name>"
        
        directory_name = args[0]
        parent_name = args[1] if len(args) > 1 else None
        parent_id = None
        directory_path = directory_name
        if not directory_name:
            return "Directory name cannot be empty."
        if parent_name:
            parent = FileService().get_directory(parent_name)
            print(parent)
            if not parent:
                return f"Parent directory '{parent_name}' already exist."
            else:
                parent_id = parent.id
                print("Parent ID",parent_id)
            directory_path = f"{parent_name}/{directory_name}"
        try:
            FileService.create_directory(directory_name, parent_id, directory_path)
            return f"Directory '{directory_name}' created successfully."
        except Exception as e:
            return f"Error creating directory: {str(e)}"