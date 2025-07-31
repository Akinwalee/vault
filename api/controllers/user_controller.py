from services.user_service import UserService
from storage.models import UserModel
from fastapi import Request, HTTPException


class UserController:
    """
    A collection of user-related operations.
    This class provides methods to handle user authentication and session management.
    """

    @staticmethod
    def get_user_id(request: Request):
        """
        Get the ID of the currently authenticated user.
        
        :return: User ID if authenticated, None otherwise.
        """
        return UserService.get_user_id()

    @staticmethod
    def is_authenticated():
        """
        Check if a user is currently authenticated.
        
        :return: True if authenticated, False otherwise.
        """
        return UserService.is_authenticated()

    @staticmethod
    def register(user_data):
        """
        Register a new user with the provided user data.
        
        :param user_data: Dictionary containing user registration details.
        :return: Confirmation message or error response.
        """
        if not user_data or len(user_data) < 3 or not all(user_data.values()):
            raise ValueError("Username, email, and password must be provided.")
        
        try:
            result = UserService.create_user(user_data)
            if isinstance(result, UserModel):
                del result.password
                return {
                    "message": f"User '{result.username}' registered successfully.",
                    "user_data": result.to_dict(),
                    "status": 200
                }
            else:
                raise HTTPException(
                    status_code=400,
                    detail=f"Error registering user: {result}"
            )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Internal server error: {str(e)}"
            )

    @staticmethod
    def login(user_data):
        """
        Log in a user with the provided credentials.
        
        :param user_data: Dictionary containing user login details.
        :return: Confirmation message or error response.
        """
        if not user_data or len(user_data) < 2 or not all(user_data.values()):
            raise ValueError("Username and password must be provided.")
        
        try:
            result = UserService.login_user(user_data['username'], user_data['password'])
            if isinstance(result, UserModel):
                del result.password
                return {
                    "message": f"User '{result.username}' logged in successfully.",
                    "user_data": result.to_dict(),
                    "status": 200
                }
            else:
                raise HTTPException(
                    status_code=401,
                    detail=f"Error logging in user: {result}"
                )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Internal server error: {str(e)}"
            )
        
    @staticmethod
    def logout():
        """
        Log out the current user.
        
        :return: Confirmation message or error response.
        """
        try:
            result = UserService.logout_user()
            return {
                "message": result,
                "status": 200
            }
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Internal server error: {str(e)}"
            )

    @staticmethod
    def get_current_user():
        """
        Get the current logged-in user.
        
        :return: User information or error response.
        """
        try:
            user = UserService.get_current_user()
            if user:
                del user.password
                return {
                    "user_data": user.to_dict(),
                    "status": 200
                }
            else:
                raise HTTPException(
                    status_code=404,
                    detail="User not found."
                )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Internal server error: {str(e)}"
            )
        
    