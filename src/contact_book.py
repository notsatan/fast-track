import logging as log
from os.path import join

from flask import Flask, jsonify, request

from .database import SQLite
from .objects import Contact


class ContactBook:
    """
    The main contact book class, instantiating an instance of this class will be enough
    to fire the main application.
    """

    def __init__(
        self, *, name: str = __name__, root_path: str, debug_mode: bool = False
    ):
        """
        Args:
            name: The `__name__` variable obtained during execution
            root_path: String containing path to the root directory
            debug_mode: Boolean indicating debug mode
        """

        self.__debug_mode = debug_mode
        self.__config_logger(
            log_file=join(root_path, "logs.txt"), debug_mode=self.__debug_mode
        )

        self.__app = Flask(import_name=name, template_folder="templates")
        self.__database = SQLite(join(root_path, "contacts.db"))

        log.debug(f'root directory: "{root_path}"')
        self.__app.add_url_rule("/post", view_func=self.add_contact, methods=["POST"])

    @staticmethod
    def __config_logger(log_file: str, debug_mode: bool) -> None:
        """
        Configure the logger to log to log file as well as console, with special
        formatting

        Args:
            log_file: String containing the name of text file to log to.
            debug_mode: Boolean indicating if the log level is set to be debug or not
        """

        if debug_mode:
            log.getLogger().setLevel(log.DEBUG)
        else:
            log.getLogger().setLevel(log.INFO)

        # Configure log formatter
        logFormatter = log.Formatter(
            "%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s"
        )

        rootLogger = log.getLogger()

        if not debug_mode:
            # Create a file handler, apply formatter and add it to the main logger.
            # Do not write to log file in debug mode - enters an infinite loop.
            fileHandler = log.FileHandler(log_file)
            fileHandler.setFormatter(logFormatter)
            rootLogger.addHandler(fileHandler)

        # Create a console handler, apply formatter and add it to the main logger.
        consoleHandler = log.StreamHandler()
        consoleHandler.setFormatter(logFormatter)
        rootLogger.addHandler(consoleHandler)

    def get_contact(self):
        """
        Handles incoming requests to fetch contacts, i.e. performs searches on the
        database, and returns the result
        """

        return jsonify({"msg": "Hello World!"})

    def add_contact(self):
        contact = Contact(
            name=request.json["name"],
            email=request.json["email"],
            phone_number=request.json["phone"],
        )

        result = self.__database.add_entry(contact)
        if result:
            return contact.stringify(indent=0), 200
        else:
            return jsonify({"error": "failure occurred"}), 500

    def run(self) -> None:
        """
        Runs the flask server.
        """

        self.__app.run(debug=self.__debug_mode)
