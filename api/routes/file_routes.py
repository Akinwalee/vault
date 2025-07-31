from controllers.file_controller import FileController
from middlewares.shared_router import router
from storage.models import CreateFileOrFolderModel




@router.post('/api/files')
async def create(data: CreateFileOrFolderModel):
    """
    Create a new file or folder with the provided file data.
    
    :param file_data: Dictionary containing file details.
    :return: Confirmation message or error response.
    """
    
    return FileController.upload_file_or_directory(data)


@router.get('/api/files')
async def get_all_files():
    """
    Retrieve all files.
    
    :return: List of files or error response.
    """
    
    return FileController.get_all_files()


@router.get('/api/files/{file_name}')
async def get_file(file_name: str):
    """
    Retrieve a file by its name.
    
    :param file_name: Name of the file to retrieve.
    :return: File content or error response.
    """
    
    return FileController.get_file(file_name)


@router.get('/api/files/{file_name}/data')
async def get_file_data(file_name: str):
    """
    Retrieve file data by its name.
    
    :param file_name: Name of the file to retrieve data for.
    :return: File data or error response.
    """
    
    return FileController.get_file_data(file_name)


@router.get('/api/file/{file_name}/thumbnail')
async def get_file_thumbnail(file_name: str):
    """
    Retrieve a thumbnail for the specified file.
    
    :param file_name: Name of the file to retrieve the thumbnail for.
    :return: Thumbnail image or error response.
    """
    
    return FileController.get_file_thumbnail(file_name)


@router.patch('/api/files/{file_name}/publish')
async def publish_file(file_name: str):
    """
    Publish a file to make it accessible to other users.
    
    :param file_name: Name of the file to publish.
    :return: Confirmation message or error response.
    """
    
    return FileController.publish_file(file_name)


@router.patch('/api/files/{file_name}/unpublish')
async def unpublish_file(file_name: str):
    """
    Unpublish a file to restrict its access.
    
    :param file_name: Name of the file to unpublish.
    :return: Confirmation message or error response.
    """
    
    return FileController.unpublish_file(file_name)