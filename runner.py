import logging as log
from configparser import ConfigParser, NoOptionError, NoSectionError
from pathlib import Path

from src import ContactBook


def db_path() -> str:
    """
    Reads the config file to return the path to database file

    Remarks:
        Will force-stop the script if the config file is invalid

    Returns:
        String containing full path to the database fill
    """

    parser = ConfigParser()
    parser.read("configs.ini")

    try:
        val = parser.get("fast-track", "root_path")

        # Replace the place-holder with the path to the current directory
        val = val.replace("{cur_dir}", str(Path(__file__).parent.absolute()))
        return val
    except (NoOptionError, NoSectionError):
        # Config file does not contain the `database` section, or the section does not
        # contain the `path` option.
        # print('Error: Invalid config file detected')
        log.error("config file is invalid")
        exit(-10)
    except Exception as e:
        # Unknown error
        log.error("unknown error occurred while reading the config file")
        log.error(f"{type(e)}\n{str(e)}")
        exit(-20)


if __name__ == "__main__":
    ContactBook(name=__name__, root_path=db_path(), debug_mode=True).run()
