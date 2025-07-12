from pymongo import MongoClient
from redis import Redis
import os
from dotenv import load_dotenv


load_dotenv()
mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
redis_host = os.getenv("REDIS_HOST", "localhost")
redis_port = int(os.getenv("REDIS_PORT", 6379))

class Database:
    """
    Database class to manage connections to Redis and MongoDB.
    """

    def __init__(self, mongo_uri=mongo_uri, redis_host=redis_host, redis_port=redis_port):
        """
        Initialize the database connections.
        
        :param mongo_uri: URI for MongoDB connection.
        :param redis_host: Host for Redis connection.
        :param redis_port: Port for Redis connection.
        """
        self.mongo_client = MongoClient(mongo_uri)
        self.redis_client = Redis(host=redis_host, port=redis_port, db=0)

    def get_mongo_db(self, db_name):
        """
        Get a MongoDB database instance.
        
        :param db_name: Name of the database to connect to.
        :return: MongoDB database instance.
        """
        return self.mongo_client[db_name]

    def get_redis_client(self):
        """
        Get the Redis client instance.
        
        :return: Redis client instance.
        """
        return self.redis_client
    
    def close_connections(self):
        """
        Close the database connections.
        """
        self.mongo_client.close()
        self.redis_client.close()
