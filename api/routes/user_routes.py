from middlewares.shared_router import router
from api.controllers.user_controller import UserController
from storage.models import RegisterModel, LoginModel


@router.post('api/register')
async def register(user_data: RegisterModel):
    """
    Register a new user with the provided user data.
    
    :param user_data: Dictionary containing user registration details.
    :return: Confirmation message or error response.
    """
   
    return UserController.register(user_data.to_dict())


@router.post('/api/login')
async def login(user_data: LoginModel):
    """
    Log in a user with the provided credentials.
    
    :param user_data: Dictionary containing user login details.
    :return: Confirmation message or error response.
    """
    
    return UserController.login(user_data.to_dict())

@router.get('/api/logout')
async def logout():
    """
    Log out the current user.
    
    :return: Confirmation message or error response.
    """
    
    return UserController.logout()

@router.get('/api/users/me')
async def get_current_user():
    """
    Get the current logged-in user.
    
    :return: User information or error response.
    """
    
    return UserController.get_current_user()
