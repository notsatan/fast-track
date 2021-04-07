from typing import Any, Dict, List, Optional

import logging as log
from sqlite3 import IntegrityError, connect

from ..objects import Contact
from .base_db import BaseDB


class SQLite(BaseDB):
    def __init__(self, db_file: str):
        """
        Args:
            db_file: String containing full path to the database file. Will be created
                if does not exist.
        """

        super().__init__(db_name="SQLite3")

        # Full path to the database file
        self.__db_instance = db_file

        self.__table_name = "contacts"
        self.__column_id = "id"
        self.__column_email = "email"
        self.__column_name = "contact_name"
        self.__column_number = "contact_number"

        # Creating the table in the database. Ignored if the table exists already
        self.__create_table()

    def __create_table(self) -> bool:
        """
        Creates the main table in the database. Will be ignored if the table exists
        already.

        Returns:
            Boolean indicating the success of the operation.
        """

        log.debug("creating table in database")
        query = f"""
            create table if not exists "{self.__table_name}" (
                "{self.__column_id}" integer primary key autoincrement,
                "{self.__column_email}" text unique not null,
                "{self.__column_name}" text not null,
                "{self.__column_number}" text unique not null
            );
        """

        with connect(self.__db_instance) as connection:
            try:
                connection.execute(query)
                connection.commit()
                return True
            except Exception as e:
                log.warning(f"failed to create table in database!")
                log.warning(f"{type(e)} \n{str(e)}")
                return False

    def execute_query(self, *args: Any, **kwargs: Any) -> None:
        """
        Not implemented
        """

        pass

    def add_entry(
        self, contact: Contact, *args: List[Any], **kwargs: Dict[Any, Any]
    ) -> bool:
        query = f"""
            insert into "{self.__table_name}"(
                "{self.__column_email}",
                "{self.__column_name}",
                "{self.__column_number}"
            ) values (?, ?, ?)
        """

        with connect(self.__db_instance) as connection:
            try:
                connection.execute(
                    query, (contact.email, contact.name, contact.phone_number)
                )

                connection.commit()
                return True
            except IntegrityError:
                log.warning(f"catch IntegrityError, failed to add data to database!")
                return False

    def remove_entry(self, *args: List[Any], **kwargs: Dict[Any, Any]) -> bool:
        pass

    def update_entry(self, *args: List[Any], **kwargs: Dict[Any, Any]) -> bool:
        pass

    def search_entry(self, *args: List[Any], **kwargs: Dict[Any, Any]) -> Optional[Any]:
        pass

    def close(self) -> None:
        pass
