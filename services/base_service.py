# Base service class that provides common functionality for all services.
from abc import ABC, abstractmethod

class BaseService(ABC):
    """
    Abstract base class for all services.
    Provides a common interface for service operations.
    """

    @abstractmethod
    def help(self):
        """
        Display help information for the service.
        """
        pass