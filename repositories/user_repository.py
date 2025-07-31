from storage.database import Database


class UserRepository:
    """
    Repository for user operations.
    Manages interactions with the database for user-related tasks.
    """
    
    def __init__(self):
        self.db = Database()
        self.mongo_db = self.db.get_mongo_db("vault")
        self.redis = self.db.get_redis_client()

    def find_by_email(self, email):
        """
        Find a user by email
        """
        try:
            user = self.mongo_db.users.find_one({"email": email})
            return user
        except Exception as e:
            return f"Error finding user: {e}"
        
    def create_user(self, user_data):
        """
        Create an entry with the user data in the database
        """
        try:
            self.mongo_db.users.insert_one(user_data)
            return None
        except Exception as e:
            return f"Error creating user in the database: {e}"

    def find_by_id(self, user_id):
        """
        Find user by id from the database
        """
        try:
            user = self.mongo_db.users.find_one({"id": user_id})
            return user
        except Exception as e:
            return f"Error finding user: {e}"
        
    def find_by_username(self, username):
        """
        Find user by username from the database
        """
        try:
            user = self.mongo_db.users.find_one({"username": username})
            return user
        except Exception as e:
            return f"Error finding user: {e}"

    def create_session(self, session_data):
        """
        Create a user session in Redis database
        """
        try:
            self.redis.hset("session", mapping=session_data)
            return None
        except Exception as e:
            return f"Error creating user session: {e}"

    def get_session(self):
        """
        Get a user session from Redis using id
        """
        try:
            session = self.redis.hgetall("session")
            return session.items()
        except Exception as e:
            return f"Error getting user session: {e}"
        
    def delete_session(self):
        """
        Delete a session data from Redis database
        """
        try:
            self.redis.delete("session")
            return None
        except Exception as e:
            return f"Error deleting session data: {e}"
        

    

        
    
