from .base_service import BaseService
import os
from utils.helpers import get_current_time, create_metadata, list_metadata, get_metadata, delete_metadata
from storage.models import FileModel, FileMetadata, FolderModel
from tempfile import NamedTemporaryFile
from services.user_service import UserService
from repositories.file_repository import FileRepository
from tasks.thumbnail import generate_thumbnail


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
            user_id = UserService.get_user_id()
            if not metadata:
                raise ValueError(f"No metadata found for file '{file_name}'.")
            if metadata.get("user_id") != user_id and metadata.get("visibility") != 'public':
                raise ValueError(f"Unauthorized access to file '{file_name}'.")
            
            with NamedTemporaryFile('+w', delete=True) as temp_file:
                temp_file = FileRepository().retrieve_file(file_name)
                if temp_file:
                    content = temp_file.decode('utf-8')
                else:
                    return ValueError(f"File '{file_name}' not found in the database.")
            return content
        
        except Exception as e:
            raise ValueError(f"Error reading file '{file_name}': {str(e)}")


    def upload_file(self, file_name, data, user_id, directory_name='root'):
        """
        Upload a file to the server.
        :param file_path: Path to the file to upload.
        :return: Confirmation of upload.
        """
        try:
            directory = self.get_directory(directory_name, user_id=user_id)
            if not isinstance(directory, dict):
                FileService().create_directory(directory_name)
                path = f"{directory_name}/{file_name}"


            file_size = os.path.getsize(data)
            file_extension = os.path.splitext(file_name)[1].lower()
            if file_extension in ['.txt', '.pdf', '.docx', '.md']:
                type = 'file'
            elif file_extension in ['.jpg', '.jpeg', '.png', '.gif']:
                type = 'image'
                generate_thumbnail.delay(data, file_name)
            elif file_extension in ['.mp4', '.avi', '.mov']:
                type = 'video'
                generate_thumbnail.delay(data, file_name)
            else:
                type = 'other'


            file_id = FileRepository().upload_file(data, file_name)


            file_metadata = FileMetadata(
                file_name=file_name,
                file_size=file_size,
                path = path,
                user_id=user_id,
                file_id=str(file_id),
                type=type,
                directory_name=directory_name,
                created_at=get_current_time()
            )
            file_model = FileModel(
                user_id=user_id,
                file_name=file_name,
                file_size=file_size,
                file_id=str(file_id),
                directory_name=directory_name,
                type=type,
                created_at=get_current_time()
            )
            FileRepository().save_file(file_model)
            result = create_metadata(file_id, file_metadata.to_dict())
            
            return result
        except Exception as e:
            raise ValueError(f"Error uploading file: {str(e)}")
        
    def list_files(self, user_id=None):
        """
        List the metadata of all files in the uploads directory.
        :return: List of files in the uploads directory.
        """
        try:
            metadata = list_metadata()
            if not metadata:
                raise ValueError("No files found.")
            
            user_id = UserService.get_user_id()
            if user_id:
                metadata = {k: v for k, v in metadata.items() if (v.get("user_id") == user_id or v.get("visibility") == 'public')}
            else:
                metadata = {k: v for k, v in metadata.items() if v.get("visibility") == 'public'}

            return metadata
        except Exception as e:
            raise ValueError(f"Error listing files: {str(e)}")

    def read_metadata(self, file_name):
        """
        Read metadata for a specific file.
        :param file_name: Name of the file to read metadata for.
        :return: Metadata dictionary for the specified file.
        """
        try:
            metadata = get_metadata(file_name)
            user_id = UserService.get_user_id()
            if not metadata:
                raise ValueError(f"No metadata found for file '{file_name}'.")
            if metadata.get("user_id") != user_id and metadata.get("visibility") != 'public':
                raise ValueError(f"Unauthorized access to metadata for file '{file_name}'.")
            return metadata
        except Exception as e:
            raise ValueError(f"Error reading metadata for file '{file_name}': {str(e)}")
        
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
                FileRepository().delete_file(file_name, file_id)
            else:
                return f"File '{file_name}' does not exist."
            delete_metadata(file_name)
            return f"File '{file_name}' deleted successfully."

        except Exception as e:
            return f"Error deleting file '{file_name}': {str(e)}"
        
    
    def publish_file(self, file_name):
        """
        Publish a file to make it accessible to all users.
        :param file_name: Name of the file to publish.
        :return: Confirmation of publication.
        """
        try:
            metadata = get_metadata(file_name)
            user_id = UserService.get_user_id()
            if not user_id:
                raise ValueError("No user session found. Cannot publish file.")
            if not metadata:
                raise ValueError(f"No metadata found for file '{file_name}'.")
            if metadata.get("user_id") != user_id:
                raise ValueError(f"Unauthorized access to publish file '{file_name}'.")
            
            metadata['visibility'] = 'public'
            create_metadata(file_name, metadata)
            
            FileRepository().update_file(file_name, metadata)
            return metadata
        
        except Exception as e:
            raise ValueError(f"Error publishing file '{file_name}': {str(e)}")
        
    def unpublish_file(self, file_name):
        """
        Unpublish a file to restrict access to the owner only.
        :param file_name: Name of the file to unpublish.
        :return: Confirmation of unpublication.
        """
        try:
            metadata = get_metadata(file_name)
            user_id = UserService.get_user_id()
            if not user_id:
                raise ValueError("No user session found. Cannot unpublish file.")
            if not metadata:
                raise ValueError(f"No metadata found for file '{file_name}'.")
            if metadata.get("user_id") != user_id:
                raise ValueError(f"Unauthorized access to unpublish file '{file_name}'.")
            
            metadata['visibility'] = 'private'
            create_metadata(file_name, metadata)
            
            FileRepository().update_file(file_name, metadata)
            return metadata
        
        except Exception as e:
            raise ValueError(f"Error unpublishing file '{file_name}': {str(e)}")

    def create_directory(self, directory_name, parent_id, directory_path='root/'):
        """
        Create a new directory.
        :param directory_name: Name of the directory to create.
        :return: Confirmation of directory creation.
        """
        try:
            user_id = UserService.get_user_id()
            directory = FileRepository().find_directory(directory_name, user_id)
            if directory and directory.parent_id == parent_id:
                raise ValueError(f"Directory '{directory_name}' already exists.")
            
            directory_path = directory_path if directory_path or directory_path == 'root/' else f'root/{directory_name}'
            new_directory = FolderModel(
                user_id=user_id,
                folder_name=directory_name,
                parent_id=parent_id,
                directory_path=directory_path,
                created_at=get_current_time()
            )
            FileRepository().create_directory(new_directory)
            return f"Directory '{directory_name}' created successfully."
        except Exception as e:
            raise ValueError(f"Error making directory '{directory_name}': {str(e)}")

    def list_directories(self, user_id=None):
        """
        List all directories for the user.
        :param user_id: ID of the user to list directories for.
        :return: List of directories.
        """
        try:
            user_id = UserService.get_user_id() if not user_id else user_id
            directories = FileRepository().get_user_directories(user_id)
            if not directories:
                return "No directories found."
            return directories
        except Exception as e:
            return f"Error listing directories: {str(e)}"

    def get_directory(self, directory_name, user_id=None):
        """
        Get details of a specific directory.
        :param directory_name: Name of the directory to retrieve.
        :return: Details of the specified directory.
        """
        try:
            user_id = UserService.get_user_id()
            directory = FileRepository().find_directory(directory_name, user_id)
            if not directory:
                raise ValueError(f"Directory '{directory_name}' not found.")
            return directory
        except Exception as e:
            raise ValueError(f"Error retrieving directory '{directory_name}': {str(e)}")
        
    
    def get_folder_files(self, directory_name):
        """
        Get all files in a specific directory.
        :param directory_name: Name of the directory to retrieve files from.
        :return: List of files in the specified directory.
        """
        try:
            user_id = UserService.get_user_id()
            metadata = list_metadata()

            if user_id:
                metadata = {k: v for k, v in metadata.items() if v.get("directory_name") == directory_name and (v.get("user_id") == user_id or v.get("visibility") == 'public')}
            else:
                metadata = {k: v for k, v in metadata.items() if v.get("directory_name") == directory_name and v.get("visibility") == 'public'}

            return metadata
        
        except Exception as e:
            return f"Error retrieving files from directory '{directory_name}': {str(e)}"
        
    