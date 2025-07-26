# Create basic database models for MongoDB
from pydantic import BaseModel, Field
from uuid import uuid4


class UserModel(BaseModel):
    """
    User model for MongoDB.
    Represents a user in the database.
    """

    id: str = Field(default_factory=lambda: str(uuid4()), description="Unique identifier for the user")
    username: str = Field(..., description="Username of the user")
    email: str = Field(..., description="Email address of the user")
    password: str = Field(..., description="Password of the user")
    created_at: str = Field(..., description="Creation timestamp of the user")

    def to_dict(self):
        """
        Convert the user model to a dictionary.
        :return: Dictionary representation of the user model.
        """
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "password": self.password,
            "created_at": self.created_at
        }

    
class FileModel(BaseModel):
    """
    File model for MongoDB.
    Represents a file in the database.
    """

    user_id: str = Field(..., description="ID of the user who uploaded the file")
    file_name: str = Field(..., description="Name of the file")
    file_size: int = Field(..., description="Size of the file in bytes")
    file_id: str = Field(...,description="The file ID from GridFS")
    created_at: str = Field(..., description="Creation timestamp of the file")
    visibility: str = Field(default='private', description="Visibility of the file (private/public)")
    type: str = Field(default='file', description="Type of the file")
    directory_name: str = Field(default=None, description="Name of the directory where the file is stored")

    def to_dict(self):
        """
        Convert the file model to a dictionary.
        :return: Dictionary representation of the file model.
        """
        return {
            "user_id": self.user_id,
            "file_name": self.file_name,
            "file_size": self.file_size,
            "file_id": self.file_id,
            "created_at": self.created_at,
            "visibility": self.visibility,
            "type": self.type,
            "directory_name": self.directory_name
        }


class FileMetadata(BaseModel):
    """
    File metadata model for MongoDB.
    Represents metadata for a file in the database.
    """

    file_name: str = Field(..., description="Name of the file")
    file_size: int = Field(..., description="Size of the file in bytes")
    path: str = Field(..., description="Path to the file on the server")
    file_path: str = Field(..., description="Path to the file in the storage system")
    user_id: str = Field(..., description="ID of the user who uploaded the file")
    file_id: str = Field(..., description="File ID from GridFS")
    visibility: str = Field(default='private', description="Visibility of the file (private/public)")
    created_at: str = Field(..., description="Creation timestamp of the file"),
    type: str = Field(default='file', description="Type of the file")
    directory_name: str = Field(default=None, description="Name of the directory where the file is stored")

    def to_dict(self):
        """
        Convert the file metadata model to a dictionary.
        :return: Dictionary representation of the file metadata model.
        """
        return {
            "file_name": self.file_name,
            "file_size": self.file_size,
            "file_path": self.file_path,
            "user_id": self.user_id,
            "file_id": self.file_id,
            "visibility": self.visibility,
            "created_at": self.created_at,
            "type": self.type,
            "directory_name": self.directory_name
        }
    
class FolderModel(BaseModel):
    """
    Folder model for MongoDB.
    Represents a folder in the database.
    """

    id: str = Field(default_factory=lambda: str(uuid4()), description="Unique identifier for the folder")
    user_id: str = Field(..., description="ID of the user who created the folder")
    folder_name: str = Field(..., description="Name of the folder")
    parent_id: str = Field(default=None, description="ID of the parent folder (if any)")
    directory_path: str = Field(..., description="Path to the folder in the storage system")
    created_at: str = Field(..., description="Creation timestamp of the folder")
    visibility: str = Field(default='private', description="Visibility of the folder (private/public)")
    
    def to_dict(self):
        """
        Convert the folder model to a dictionary.
        :return: Dictionary representation of the folder model.
        """
        return {
            "id": self.id,
            "user_id": self.user_id,
            "folder_name": self.folder_name,
            "parent_id": self.parent_id,
            "directory_path": self.directory_path,
            "created_at": self.created_at,
            "visibility": self.visibility
        }