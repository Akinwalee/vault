from .base_service import BaseService
import os
import shutil
from utils.helpers import get_current_time, create_metadata

class FileService(BaseService):
    """
    Service for file operations.
    Inherits from BaseService to provide common functionality.
    """

    def help(self):
        """
        Display help information for file operations.
        """
        return """
            FileService: Use this service to perform file operations like reading, uploading, listing and deleting files."""

    def read_file(self, file_path):
        """
        Read the contents of a file.
        :param file_path: Path to the file to read.
        :return: Contents of the file.
        """
        pass

    def upload_file(self, file_path):
        """
        Upload a file to the server.
        :param file_path: Path to the file to upload.
        :return: Confirmation of upload.
        """
        try:
            file_name = file_path.split('/')[-1]
            file_size = os.path.getsize(file_path)
            print(file_path)
            destination_path = f"storage/uploads/{file_name}"
            shutil.copy(file_path, destination_path)
            data = {
                "created_at": get_current_time(),
                "file_name": file_name,
                "file_size": file_size,
                "file_path": destination_path
            }
            result = create_metadata(file_name, data)
            if result:
                return f"File '{file_name}' uploaded successfully to {destination_path}."
        except Exception as e:
            return f"Error uploading file: {str(e)}"