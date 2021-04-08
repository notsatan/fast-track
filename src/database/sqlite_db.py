from typing import Any, Dict, List, Optional, Tuple, Union

import logging as log
from sqlite3 import IntegrityError, connect

from cachetools import TTLCache, cached

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
                "{self.__column_email}" text primary key,
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

    def execute_query(self, query: str, *args: Any, **kwargs: Any) -> None:
        with connect(self.__db_instance) as connection:
            connection.execute(query)
            connection.commit()

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
                log.warning(f"catch IntegrityError, failed to add data")
                return False
            except Exception as e:
                log.warning(f"unknown exception raised while adding a contact")
                log.warning(f"exception type: {type(e)}\n{str(e)}")
                return False

    def remove_entry(
        self, email: str, *args: List[Any], **kwargs: Dict[Any, Any]
    ) -> Union[bool, int]:
        query = f"""
            delete from "{self.__table_name}" where
            "{self.__column_email}"=?
        """

        with connect(self.__db_instance) as connection:
            try:
                cursor = connection.cursor()
                cursor.execute(query, (email,))
                connection.commit()
                return int(cursor.rowcount)  # return the number of rows affected
            except Exception as e:
                log.warning(f"failed to remove row from database")
                log.warning(f"exception type: {type(e)}\n{str(e)}")
                return False

    def update_entry(
        self, email: str, update: Contact, *args: List[Any], **kwargs: Dict[Any, Any]
    ) -> Union[int, bool]:
        query = f"""
            update "{self.__table_name}" set
            """

        placeholder: List[str] = []

        for key, val in {
            self.__column_email: update.email,
            self.__column_name: update.name,
            self.__column_number: update.phone_number,
        }.items():
            if val:
                query += f'{"," if len(placeholder) > 0 else ""}"{key}"=?'
                placeholder.append(val)

        query += f"""
            where "{self.__column_email}"=?
        """
        placeholder.append(email)

        with connect(self.__db_instance) as connection:
            try:
                cursor = connection.cursor()
                cursor.execute(query, tuple(placeholder))
                connection.commit()
                return int(cursor.rowcount)  # return the number of rows affected
            except Exception as e:
                log.warning(f"failed to update row in database")
                log.warning(f"exception type: {type(e)}\n{str(e)}")
                return False

    # Cache upto 100 search results for 300 seconds
    @cached(cache=TTLCache(maxsize=100, ttl=30))
    def search_entry(
        self,
        name: Optional[str] = "",
        email: Optional[str] = "",
        *args: List[Any],
        **kwargs: Dict[Any, Any],
    ) -> Optional[Any]:
        if not name and not email:
            # If both name and email are absent, return an empty response.
            return None

        # Forming an incomplete query, the contents of the where clause will be
        # added later.
        query = f"""
            select
            "{self.__column_email}",
            "{self.__column_name}",
            "{self.__column_number}"
        from "{self.__table_name}" where
        """

        if name and not email:
            # Search by name
            query += f'"{self.__column_name}" like ?'
            placeholder: Tuple[str, ...] = (f"%{name}%",)
        elif email and not name:
            # Search by email - will return a single result at most
            query += f'"{self.__column_email}"=?'
            placeholder = (email,)  # assignment: ignore
        else:
            # If both name and email are supplied, combine them with the `and` operator
            query += f'"{self.__column_email}"=? and "{self.__column_name}" like ?'
            placeholder = (str(email), f"%{name}%")

        with connect(self.__db_instance) as connection:
            cursor = connection.cursor()
            cursor.execute(query, placeholder)

            rows = cursor.fetchall()
            result = []
            for element in rows:
                if len(element) < 3:
                    continue

                result.append(
                    Contact(email=element[0], name=element[1], phone_number=element[2])
                )

            return result

    def close(self) -> None:
        pass
