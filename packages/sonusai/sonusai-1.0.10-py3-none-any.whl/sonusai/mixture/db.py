import contextlib
import sqlite3
from os import remove
from os.path import exists
from sqlite3 import Connection
from sqlite3 import Cursor
from typing import Any

from .. import logger_db
from .db_file import db_file


class SQLiteDatabase:
    """A context manager for SQLite database connections with configurable behavior."""

    # Constants for database configuration
    READONLY_MODE = "?mode=ro"
    WRITE_OPTIMIZED_PRAGMAS = (
        "?_journal_mode=OFF&_synchronous=OFF&_cache_size=10000&_temp_store=MEMORY&_locking_mode=EXCLUSIVE"
    )
    CONNECTION_TIMEOUT = 20

    def __init__(
        self,
        location: str,
        create: bool = False,
        readonly: bool = True,
        test: bool = False,
        verbose: bool = False,
    ) -> None:
        """Initialize SQLite database connection manager.

        Args:
            location: Path to the database file.
            create: If True, create a new database file, overwriting any existing one.
            readonly: If True, open the database in read-only mode.
            test: If True, use the test database path.
            verbose: If True, enable SQL statement logging.
        """
        self.location = location
        self.create = create
        self.readonly = readonly
        self.test = test
        self.verbose = verbose
        self.con: Connection | None = None
        self.cur: Cursor | None = None

    def __enter__(self) -> Cursor:
        """Enter the context manager, establishing the database connection.

        Returns:
            A database cursor for executing queries.

        Raises:
            sqlite3.Error: If connection fails.
        """
        try:
            self._establish_connection()
        except Exception:
            self._close_resources()
            raise

        if self.cur:
            return self.cur
        raise sqlite3.Error("Failed to connect to database")

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: Any | None,
    ) -> None:
        """Exit the context manager, committing changes if appropriate and closing resources.

        Args:
            exc_type: The exception type, if any.
            exc_val: The exception value, if any.
            exc_tb: The exception traceback, if any.
        """
        if self.con:
            if exc_type is None and not self.readonly:
                # Commit only on successful exit if not readonly
                self.con.commit()
            self._close_resources()

    def _close_resources(self) -> None:
        """Safely close database cursor and connection resources."""
        if self.cur:
            with contextlib.suppress(sqlite3.Error):
                self.cur.close()
            self.cur = None

        if self.con:
            with contextlib.suppress(sqlite3.Error):
                self.con.close()
            self.con = None

    def _establish_connection(self) -> None:
        """Establish a connection to the SQLite database.

        Raises:
            OSError: If the database file doesn't exist and create=False.
            sqlite3.Error: If connection to the database fails.
        """
        db_path = self._get_db_path()
        self._prepare_db_file(db_path)
        uri = self._build_connection_uri(db_path)

        try:
            self.con = sqlite3.connect(f"file:{uri}", uri=True, timeout=self.CONNECTION_TIMEOUT)
            if self.verbose and self.con:
                self.con.set_trace_callback(logger_db.debug)
        except sqlite3.Error as e:
            raise sqlite3.Error(f"Failed to connect to database: {e}") from e

        self.cur = self.con.cursor()

    def _get_db_path(self) -> str:
        """Get the database file path based on location and test settings.

        Returns:
            The path to the database file.
        """
        return db_file(self.location, self.test)

    def _prepare_db_file(self, db_path: str) -> None:
        """Prepare the database file based on creation settings.

        Args:
            db_path: Path to the database file.

        Raises:
            OSError: If the database file doesn't exist and create=False.
        """
        if self.create and exists(db_path):
            remove(db_path)

        if not self.create and not exists(db_path):
            raise OSError(f"Could not find mixture database in {self.location}")

    def _build_connection_uri(self, db_path: str) -> str:
        """Build the SQLite connection URI with appropriate options.

        Args:
            db_path: Path to the database file.

        Returns:
            A properly formatted SQLite URI with appropriate options.
        """
        uri = db_path

        # Add readonly mode if needed
        if not self.create and self.readonly:
            uri += self.READONLY_MODE

        # Add optimized pragmas for write mode
        if not self.readonly:
            if "?" in uri:
                uri = uri.replace("?", f"{self.WRITE_OPTIMIZED_PRAGMAS}&")
            else:
                uri += self.WRITE_OPTIMIZED_PRAGMAS

        return uri
