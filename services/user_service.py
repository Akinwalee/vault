from .base_service import BaseService
from storage.database import Database
from storage.models import UserModel
from uuid import uuid4
import bcrypt



db = Database()
mongo_db = db.get_mongo_db("vault")
redis = db.get_redis_client()


class UserService(BaseService):
    """
    Service for user operations.
    Inherits from BaseService to provide common functionality.
    """

    def help(self):
        """
        Display help information for user operations.
        """
        return """
            UserService: Use this service to perform user operations like authentication, registration, and profile management."""
    
    async def create_user(self, user: UserModel):
        """
        Create a new user.
        :param user_data: Dictionary containing user information.
        :return: Confirmation of user creation.
        """
        try:
            id = str(uuid4())
            user_data = user.to_dict()
            hash = bcrypt.hashpw(user_data['password'].encode('utf-8'), bcrypt.gensalt())
            user_data['password'] = hash.decode('utf-8')
            user_data['id'] = id
            user_data['created_at'] = user_data.get('created_at', str(uuid4()))
            await mongo_db.users.insert_one(user_data)
            return f"User '{user_data['username']}' created successfully."
        except Exception as e:
            return f"Error creating user: {str(e)}"
        
    async def get_current_user(self):
        """
        Get the current user from the session.
        :return: User information if session exists, otherwise None.
        """
        try:
            session = redis.get("session")
            if session:
                user_id = session.get("user_id")
                if user_id:
                    user_data = await mongo_db.users.find_one({"id": user_id})
                    if user_data:
                        return UserModel(**user_data)
            return None
        except Exception as e:
            return f"Error retrieving user: {str(e)}"
        
    async def authenticate_user(self, username: str, password: str):
        """
        Authenticate a user with username and password.
        :param username: Username of the user.
        :param password: Password of the user.
        :return: User information if authentication is successful, otherwise None.
        """
        try:
            user_data = await mongo_db.users.find_one({"username": username})
            if user_data and bcrypt.checkpw(password.encode('utf-8'), user_data['password'].encode('utf-8')):
                return UserModel(**user_data)
            return None
        except Exception as e:
            return f"Error authenticating user: {str(e)}"
        
    async def login_user(self, username: str, password: str):
        """
        Log in a user by setting the session.
        :param username: Username of the user.
        :param password: Password of the user.
        :return: Confirmation of login or error message.
        """
        try:
            user = await self.authenticate_user(username, password)
            if user:
                session_data = {"user_id": user.id, "token": str(uuid4())}
                redis.set("session", session_data)
                return f"User '{username}' logged in successfully."
            else:
                return "Invalid username or password."
        except Exception as e:
            return f"Error logging in user: {str(e)}"
        
    async def logout_user(self):
        """
        Log out the current user by clearing the session.
        :return: Confirmation of logout.
        """
        try:
            redis.delete("session")
            return "User logged out successfully."
        except Exception as e:
            return f"Error logging out user: {str(e)}"