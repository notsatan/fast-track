"""
Defines the an abstract database class - meant to be used as the base class from which
all databases should inherit.
"""

from typing import Any, Optional

import logging as logger
from abc import ABC, abstractmethod

from ..objects import Contact


class BaseDB(ABC):
    """
    Abstract parent class for all databases. Defines common attributes for child
    classes. Abstract methods ensure that the child class will need to implement them.

    Attributes:
    -----------
        db_name: str
            Property to get the internal name for the database. Can be used in log
            messages and stuff.

    Methods:
    --------
        execute_query(any, any)
            Executes raw queries on the database. Not all sub-classes will implement
            this

        add_entry(any, any)
            Add a new entry to the database

        remove_entry(any, any)
            Remove an entry from the database

        update_entry(any, any)
            Update an existing entry from the database

        search_entry(any, any)
            Search for an existing entry in the database

        close()
            Closes the connection to the database
    """

    def __init__(self, db_name: str):
        """
        Args:
            db_name: String containing a friendly name for the database, used for
                logging and similar purposes.
        """

        self.__db_instance = db_name
        logger.debug(f"Initializing an instance of database `{self.__db_instance}`")

    @abstractmethod
    def execute_query(self, *args: Any, **kwargs: Any) -> Any:
        """
        Executes raw queries on the database, returning the result.

        Note: Can be deprecated if the database does not allow executing raw queries.

        Args:
            *args: List of parameters to be added
            **kwargs: Named input parameters to be added to the database

        Returns:
            None if the database does not allow queries, or the result of the query.
        """

        pass

    @abstractmethod
    def add_entry(self, contact: Contact, *args: Any, **kwargs: Any) -> bool:
        """
        Add entries to the database.

        Args:
            contact: The contact to be added
            *args: List of parameters to be added
            **kwargs: Named input parameters to be added to the database

        Returns:
            True if successful, false otherwise.
        """

        pass

    @abstractmethod
    def remove_entry(self, *args: Any, **kwargs: Any) -> bool:
        """
        Remove entries from the database.

        Args:
            *args: List of parameters to be added
            **kwargs: Named input parameters to be added to the database

        Returns:
            True if successful, false otherwise.
        """

        pass

    @abstractmethod
    def update_entry(self, *args: Any, **kwargs: Any) -> bool:
        """
        Update an existing entry from the database.

        Args:
            *args: List of parameters to be added
            **kwargs: Named input parameters to be added to the database

        Returns:
            True if successful, false otherwise.
        """

        pass

    @abstractmethod
    def search_entry(self, *args: Any, **kwargs: Any) -> Optional[Any]:
        """
        Search for existing entries in database.

        Args:
            *args: List of parameters to be added
            **kwargs: Named input parameters to be added to the database

        Returns:
            The row, if found. None otherwise.
        """

        pass

    @abstractmethod
    def close(self) -> None:
        """
        Closes the connection to the database.
        """

        pass

    @property
    def db_name(self):
        return self.__db_instance
