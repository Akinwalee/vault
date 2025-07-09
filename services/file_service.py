from .base_service import BaseService
import os
import shutil
from utils.helpers import get_current_time, create_metadata, list_metadata, get_metadata, delete_metadata
import uuid

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

    def read_file(self, file_name):
        """
        Read the contents of a file.
        :param file_path: Name of the file to read.
        :return: Content of the file.
        """
        try:
            metadata = get_metadata(file_name)
            if metadata:
                file_path = metadata.get("file_path")
                if not os.path.exists(file_path):
                    return f"File '{file_name}' does not exist at {file_path}."
                with open(file_path, 'r') as file:
                    content = file.read()
                return content
            else:
                return f"No metadata found for file '{file_name}'."
        except Exception as e:
            return f"Error reading file '{file_name}': {str(e)}"


    def upload_file(self, file_path):
        """
        Upload a file to the server.
        :param file_path: Path to the file to upload.
        :return: Confirmation of upload.
        """
        try:
            file_name = file_path.split('/')[-1]
            file_size = os.path.getsize(file_path)
            
            destination_path = f"storage/uploads/{file_name}"
            shutil.copy(file_path, destination_path)
            data = {
                "created_at": get_current_time(),
                "file_name": file_name,
                "file_size": file_size,
                "file_path": destination_path,
                "id": f"{uuid.uuid4()}"
            }
            result = create_metadata(file_name, data)
            if result:
                return f"File '{file_name}' uploaded successfully to {destination_path}."
        except Exception as e:
            return f"Error uploading file: {str(e)}"
        
    def list_files(self):
        """
        List the metadata of all files in the uploads directory.
        :return: List of files in the uploads directory.
        """
        try:
            metadata = list_metadata()

            return metadata
        except Exception as e:
            return f"Error listing files: {str(e)}"

    def read_metadata(self, file_name):
        """
        Read metadata for a specific file.
        :param file_name: Name of the file to read metadata for.
        :return: Metadata dictionary for the specified file.
        """
        try:
            metadata = get_metadata(file_name)
            if metadata:
                return metadata
            else:
                return f"No metadata found for file '{file_name}'."
        except Exception as e:
            return f"Error reading metadata for file '{file_name}': {str(e)}"
        
    def delete_file(self, file_name):
        """
        Delete a file from the server.
        :param file_name: Name of the file to delete.
        :return: Confirmation of deletion.
        """
        try:
            metadata = get_metadata(file_name)
            if metadata:
                file_path = metadata.get("file_path")
                if os.path.exists(file_path):
                    os.remove(file_path)
                else:
                    return f"File '{file_name}' does not exist at {file_path}."
                delete_metadata(file_name)
                return f"File '{file_name}' deleted successfully."
            else:
                return f"No metadata found for file '{file_name}'."
        except Exception as e:
            return f"Error deleting file '{file_name}': {str(e)}"
