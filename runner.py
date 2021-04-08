from typing import Tuple

import logging as log
from configparser import ConfigParser, NoOptionError, NoSectionError
from pathlib import Path

from src import ContactBook


def read_configs() -> Tuple[str, bool]:
    """
    Reads the config file and return the values found

    Remarks:
        Will force-stop the script if the config file is invalid

    Returns:
        Tuple containing the values from the config file
    """

    parser = ConfigParser()
    parser.read("configs.ini")

    try:
        root_path = parser.get("fast-track", "root_path")
        debug_mode = parser.get("fast-track", "debug")

        debug = True if debug_mode == "true" else False

        # Replace the place-holder with the path to the current directory
        root_path = root_path.replace(
            "{cur_dir}", str(Path(__file__).parent.absolute())
        )
        return root_path, debug
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
    configs = read_configs()
    ContactBook(name=__name__, root_path=configs[0], debug_mode=configs[1]).run()
