"""
Defines base contact class.
"""

from typing import Dict

from json import dumps as prettify_json


class Contact:
    """
    The base contact class. Each instance of this class will represent an individual
    contact in the memory.

    Attributes:
    -----------
        name: str
            Name of the contact

        email: str
            eMail ID of the contact. Will be unique across the database

        phone_number: str
            Phone number of the contact. Unique across the database

    Methods:
    --------
        stringify(int) -> str
            Returns a JSON string representation of the data held by the class instance
            with required indentation.
    """

    def __init__(self, name: str, email: str, phone_number: str):
        """
        Args:
            name: String containing the name of the contact
            email: String containing the email id
            phone_number: String containing the phone number
        """

        self.name = name
        self.email = email
        self.phone_number = phone_number

    def stringify(self, indent: int = 4) -> str:
        """
        A simple attribute to convert the class into a JSON string. Private variables,
        and methods are ignored.

        Args:
            indent: Integer containing the number of indents required. Use zero for a
                machine-readable JSON string.

        Returns:
            String containing JSON representation of the class instance.
        """

        return prettify_json(
            obj={
                key: value
                for key, value in self.__dict__.items()
                if not key.startswith("_") and not callable(key)
            },
            indent=indent if indent != 0 else None,
            sort_keys=True,
        )

    def encode(self) -> Dict[str, str]:
        """
        Method to convert the class instance into a dictionary of key-value pairs.
        Designed to make the class object be serializable

        Returns:
            Dictionary of string based key-value pairs, with the key being the name
            of the variable in the class, and the value being the value held in the
            instance.
        """

        return {
            key: value
            for key, value in self.__dict__.items()
            if not key.startswith("_") and not callable(key)
        }

    def __str__(self) -> str:
        return self.stringify(indent=0)
