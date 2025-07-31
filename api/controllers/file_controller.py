from services.file_service import FileService
from storage.models import CreateFileOrFolderModel
from fastapi import HTTPException


class FileController:
    """
    A collection of file-related operations.
    This class provides methods to handle file uploads, directory management, and file listing.
    """

    @staticmethod
    def upload_file_or_directory(data: CreateFileOrFolderModel, user_id: str):
        """
        Upload a file or create a directory.
        
        :param file_name: Name of the file or directory.
        :param data: Data to be uploaded (if applicable).
        :param directory_name: Name of the directory where the file should be stored.
        :param user_id: ID of the user uploading the file.
        :return: Confirmation message or error response.
        """
        if data.type in ['file', 'image']:
            file_data = data.to_file_data()
            try:
                result = FileService.upload_file(file_data['file_name'], file_data['data'], user_id, data.directory_name)
                if isinstance(result, str):
                    return {
                        "message": f"File '{file_data['file_name']}' uploaded successfully.",
                        "status": 201
                    }
            except ValueError as e:
                return {
                    "message": str(e),
                    "status": 400
                }
        elif data.type == 'folder':
            folder_data = data.to_folder_data()
            try:
                parent = FileService().get_directory(data.parent_name)
                if not parent:
                    raise ValueError(f"Parent directory '{data.parent_name}' does not exist.")
                
                directory_path = f"{data.parent_name}/{folder_data['directory_name']}"

                result = FileService.create_directory(folder_data['directory_name'], parent.id, directory_path)
                if isinstance(result, str):
                    return {
                        "message": f"Directory '{folder_data['folder_name']}' created successfully.",
                        "status": 201
                    }
            except ValueError as e:
                return {
                    "message": str(e),
                    "status": 400
                }
        else:
            raise HTTPException(
                status_code=400,
                detail="Invalid type. Must be 'file', 'image', or 'folder'."
            )

    @staticmethod
    def get_file(file_name: str):
        """
        Retrieve a file by its name.
        
        :param file_name: Name of the file to retrieve.
        :return: File content or error response.
        """
        try:
            metadata = FileService.read_metadata(file_name)
            if not metadata:
                raise HTTPException(
                    status_code=404,
                    detail=f"File '{file_name}' not found."
                )
            return {
                "file_content": metadata,
                "status": 200
            }
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Internal server error: {str(e)}"
            )

    @staticmethod
    def get_all_files():
        """
        Retrieve all files.
        
        :return: List of files or error response.
        """
        try:
            files = FileService.list_files()
            if not files or not isinstance(files, dict):
                raise HTTPException(
                    status_code=404,
                    detail="No files found."
                )
            return {
                "message": "Files retrieved successfully.",
                "data": files,
                "status": 200
            }
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Internal server error: {str(e)}"
            )

    @staticmethod
    def publish_file(file_name: str):
        """
        Publish a file to make it accessible to other users.
        
        :param file_name: Name of the file to publish.
        :return: Confirmation message or error response.
        """
        try:
            result = FileService.publish_file(file_name)
            if isinstance(result, dict):
                return {
                    "message": f"File '{file_name}' published successfully.",
                    "data": result,
                    "status": 200
                }
            else:
                raise HTTPException(
                    status_code=400,
                    detail=f"Error publishing file '{file_name}': {result}"
                )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Internal server error: {str(e)}"
            )
        
    @staticmethod
    def unpublish_file(file_name: str):
        """
        Unpublish a file to restrict its visibility.
        
        :param file_name: Name of the file to unpublish.
        :return: Confirmation message or error response.
        """
        try:
            result = FileService.unpublish_file(file_name)
            if isinstance(result, dict):
                return {
                    "message": f"File '{file_name}' unpublished successfully.",
                    "data": result,
                    "status": 200
                }
            else:
                raise HTTPException(
                    status_code=400,
                    detail=f"Error unpublishing file '{file_name}': {result}"
                )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Internal server error: {str(e)}"
            )

    @staticmethod
    def get_file_data(file_name: str):
        """
        Retrieve file data by its name.
        
        :param file_name: Name of the file to retrieve data for.
        :return: File data or error response.
        """
        try:
            data = FileService.read_file(file_name)
            if not data:
                raise HTTPException(
                    status_code=404,
                    detail=f"File data for '{file_name}' not found."
                )
            return {
                "message": f"File data retrieve successfully",
                "data": data,
                "status": 200
            }
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Internal server error: {str(e)}"
            )