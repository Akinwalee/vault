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

    def to_dict(self):
        """
        Convert the file model to a dictionary.
        :return: Dictionary representation of the file model.
        """
        return {
            "user_id": self.user_id,
            "file_name": self.file_name,
            "file_size": self.file_size,
            "file": self.file_id,
            "created_at": self.created_at
        }


class FileMetadata(BaseModel):
    """
    File metadata model for MongoDB.
    Represents metadata for a file in the database.
    """

    file_name: str = Field(..., description="Name of the file")
    file_size: int = Field(..., description="Size of the file in bytes")
    file_path: str = Field(..., description="Path to the file on the server")
    file_id: str = Field(..., description="File ID from GridFS")
    created_at: str = Field(..., description="Creation timestamp of the file")