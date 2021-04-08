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
        self.__app.add_url_rule(
            "/update", view_func=self.edit_contact, methods=["POST"]
        )
        self.__app.add_url_rule(
            "/search", view_func=self.search_contact, methods=["GET"]
        )
        self.__app.add_url_rule(
            "/delete", view_func=self.remove_contact, methods=["DELETE"]
        )

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

    def remove_contact(self):
        """
        Handles DELETE Requests to delete an existing contact from the database.
        """

        email = request.json.get("email", None)
        if not email:
            # Throw an error if email field is not present, or empty
            return jsonify({"error": "malformed request"}), 400

        result = self.__database.remove_entry(email=email)
        if result:
            return jsonify({"result": "deleted contact successfully"}), 200
        else:
            return jsonify({"error": "internal error occurred"}), 500

    def add_contact(self):
        """
        Handles incoming POST Requests to add a new contact to the database.
        The request contents should contain details about the new contact to add in
        JSON format.
        """

        contact = Contact(
            name=request.json.get("name", None),
            email=request.json.get("email", None),
            phone_number=request.json.get("phone", ""),
        )

        if not contact.email or not contact.name:
            # Throw an error if either name or email are not present/empty
            return jsonify({"error": "malformed request"}), 400

        result = self.__database.add_entry(contact)
        if result:
            return contact.stringify(indent=0), 200
        else:
            return jsonify({"error": "failure occurred"}), 500

    def search_contact(self):
        """
        Search for a contact using their name or email id
        """

        name = request.json.get("name", None)
        email = request.json.get("email", None)

        if not name and not email:
            # Throw an error if both name and email are absent
            return jsonify({"error": "malformed request"}), 400

        result = self.__database.search_entry(email=email, name=name)
        if isinstance(result, list):
            # Checking for type of `result` to ensure that a blank search result doesn't
            # enter the `else` block
            return jsonify([res.encode() for res in result]), 200
        else:
            return jsonify({"error": "internal error"}), 200

    def edit_contact(self):
        """
        Edit an existing contact
        """

        email = request.json.get("email", None)
        if not email:
            return jsonify({"error": "malformed request"}), 400

        contact = Contact(
            name=request.json.get("new_name", ""),
            email=request.json.get("new_email", ""),
            phone_number=request.json.get("new_phone", ""),
        )

        result = self.__database.update_entry(email=email, update=contact)
        if result:
            return jsonify({"result": "contact modified successfully"}), 200
        else:
            return jsonify({"error": "internal error"}), 500

    def run(self) -> None:
        """
        Runs the flask server.
        """

        self.__app.run(debug=self.__debug_mode)
