from .base_service import BaseService
from storage.database import Database
from storage.models import UserModel
from uuid import uuid4
import bcrypt


class UserService(BaseService):
    """
    Service for user operations.
    Inherits from BaseService to provide common functionality.
    """

    db = Database()
    mongo_db = db.get_mongo_db("vault")
    redis = db.get_redis_client()

    @classmethod
    def help(cls):
        """
        Display help information for user operations.
        """
        return """
            UserService: Use this service to perform user operations like authentication, registration, and profile management.
            """
    
    @classmethod
    def create_user(cls, user: UserModel):
        """
        Create a new user.
        :param user_data: Dictionary containing user information.
        :return: Confirmation of user creation.
        """
        try:
            id = str(uuid4())
            user_data = user.to_dict()
            existing_user = cls.mongo_db.users.find_one({"email": user_data['email']})
            if existing_user:
                return "A user with that email already exists"
            
            hash = bcrypt.hashpw(user_data['password'].encode('utf-8'), bcrypt.gensalt())
            user_data['password'] = hash.decode('utf-8')
            user_data['id'] = id
            user_data['created_at'] = user_data.get('created_at', str(uuid4()))
            cls.mongo_db.users.insert_one(user_data)
            return f"User '{user_data['username']}' created successfully."
        except Exception as e:
            return f"Error creating user: {str(e)}"
        
    @classmethod
    def get_current_user(cls):
        """
        Get the current user from the session.
        :return: User information if session exists, otherwise None.
        """
        try:
            session = {k.decode('utf-8'): v.decode('utf-8') for k, v in cls.redis.hgetall("session").items()}
            if session:
                user_id = session.get("user_id")
                if user_id:
                    user_data = cls.mongo_db.users.find_one({"id": user_id})
                    if user_data:
                        return UserModel(**user_data)
            return None
        except Exception as e:
            return f"Error retrieving user: {str(e)}"
    
    @classmethod
    def authenticate_user(cls, username: str, password: str):
        """
        Authenticate a user with username and password.
        :param username: Username of the user.
        :param password: Password of the user.
        :return: User information if authentication is successful, otherwise None.
        """
        try:
            user_data = cls.mongo_db.users.find_one({"username": username})
            if user_data and bcrypt.checkpw(password.encode('utf-8'), user_data['password'].encode('utf-8')):
                return UserModel(**user_data)
            return None
        except Exception as e:
            return f"Error authenticating user: {str(e)}"
        
    @classmethod
    def login_user(cls, username: str, password: str):
        """
        Log in a user by setting the session.
        :param username: Username of the user.
        :param password: Password of the user.
        :return: Confirmation of login or error message.
        """
        try:
            user = cls.authenticate_user(username, password)
            if user:
                session_data = {"user_id": user.id, "token": str(uuid4())}
                cls.redis.hset("session", mapping=session_data)
                return f"User '{username}' logged in successfully."
            else:
                return "Invalid username or password."
        except Exception as e:
            return f"Error logging in user: {str(e)}"
        
    @classmethod
    def logout_user(cls):
        """
        Log out the current user by clearing the session.
        :return: Confirmation of logout.
        """
        try:
            cls.redis.delete("session")
            return "User logged out successfully."
        except Exception as e:
            return f"Error logging out user: {str(e)}"
        
    @classmethod
    def get_user_id(cls):
        """
        Get the user ID from the current session.
        :return: User ID if session exists, otherwise None.
        """
        try:
            session = {k.decode('utf-8'): v.decode('utf-8') for k, v in cls.redis.hgetall("session").items()}
            if session:
                return session.get("user_id")
            return None
        except Exception as e:
            return f"Error retrieving user ID: {str(e)}"
