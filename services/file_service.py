from .base_service import BaseService
import os
import shutil
from utils.helpers import get_current_time, create_metadata, list_metadata, get_metadata, delete_metadata
import uuid
from storage.database import Database
from storage.models import FileModel, FileMetadata
import gridfs
from tempfile import NamedTemporaryFile
from services.user_service import UserService


class FileService(BaseService):
    """
    Service for file operations.
    Inherits from BaseService to provide common functionality.
    """
    db = Database()
    mongo_db = db.get_mongo_db("vault")
    redis = db.get_redis_client()
    fs = gridfs.GridFS(mongo_db, collection="files")

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
            user_id = UserService.get_user_id()
            if not user_id:
                return "No user session found. Cannot read file."
            if not metadata:
                return f"No metadata found for file '{file_name}'."
            if metadata.get("user_id") != user_id:
                return f"Unauthorized access to file '{file_name}'."
            
            with NamedTemporaryFile('+w', delete=True) as temp_file:
                temp_file = self.fs.find_one({"filename": file_name})
                if temp_file:
                    content = temp_file.read().decode('utf-8')
                else:
                    return f"File '{file_name}' not found in the database."
            return content
        
        except Exception as e:
            return f"Error reading file '{file_name}': {str(e)}"


    async def upload_file(self, file_path):
        """
        Upload a file to the server.
        :param file_path: Path to the file to upload.
        :return: Confirmation of upload.
        """
        try:
            file_name = file_path.split('/')[-1]
            file_size = os.path.getsize(file_path)

            with open(file_path, 'rb') as file:
                file_id = self.fs.put(file, filename=file_name, content_type='application/octet-stream')


            file_metadata = FileMetadata(
                file_name=file_name,
                file_size=file_size,
                file_path=file_path,
                file_id=str(file_id),
                created_at=get_current_time()
            )
            file_model = FileModel(
                user_id=self.redis.get("session").get("user_id"),
                file_name=file_name,
                file_size=file_size,
                file_id=str(file_id),
                created_at=get_current_time()
            )
            await self.mongo_db.files.insert_one(file_model.to_dict())
            result = create_metadata(file_name, file_metadata.to_dict())
            if result:
                return f"File '{file_name}' uploaded successfully."
        except Exception as e:
            return f"Error uploading file: {str(e)}"
        
    def list_files(self):
        """
        List the metadata of all files in the uploads directory.
        :return: List of files in the uploads directory.
        """
        try:
            metadata = list_metadata()
            if not metadata:
                return "No files found."
            
            user_id = UserService.get_user_id()
            if user_id:
                metadata = {k: v for k, v in metadata.items() if v.get("user_id") == user_id}
            else:
                return "No user session found. Cannot list files."

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
            user_id = UserService.get_user_id()
            if not user_id:
                return "No user session found. Cannot read metadata."
            if not metadata:
                return f"No metadata found for file '{file_name}'."
            if metadata.get("user_id") != user_id:
                return f"Unauthorized access to metadata for file '{file_name}'."
            return metadata
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
            user_id = UserService.get_user_id()
            if not user_id:
                return "No user session found. Cannot delete file."
            if not metadata:
                return f"No metadata found for file '{file_name}'."
            if metadata.get("user_id") != user_id:
                return f"Unauthorized access to delete file '{file_name}'."
            
            file_id = metadata.get("file_id")
            if file_id:
                self.fs.delete(file_id)
                file_path = metadata.get("file_path")
                if file_path and os.path.exists(file_path):
                    os.remove(file_path)
            else:
                return f"File '{file_name}' does not exist at {file_path}."
            delete_metadata(file_name)
            return f"File '{file_name}' deleted successfully."

        except Exception as e:
            return f"Error deleting file '{file_name}': {str(e)}"
