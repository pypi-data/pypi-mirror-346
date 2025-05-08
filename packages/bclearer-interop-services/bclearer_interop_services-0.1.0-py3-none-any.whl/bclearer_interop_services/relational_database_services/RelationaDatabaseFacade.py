from abc import ABC, abstractmethod


# Abstract base class for the database facade
class DatabaseFacade(ABC):
    def __init__(
        self,
        host,
        database,
        user,
        password,
    ):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.connection = None

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def disconnect(self):
        pass

    @abstractmethod
    def execute_query(
        self,
        query,
        params=None,
    ):
        pass

    @abstractmethod
    def fetch_results(
        self,
        query,
        params=None,
    ):
        pass
