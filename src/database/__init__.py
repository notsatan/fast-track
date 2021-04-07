"""
Package containing implementations of the database(s) being used in the back-end.
Designed following the open-close principle, allows to decouple the rest of the
application from the database.
"""

from .sqlite_db import SQLite
