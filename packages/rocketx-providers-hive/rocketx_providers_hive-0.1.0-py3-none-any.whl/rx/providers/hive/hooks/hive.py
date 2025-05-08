import sqlparse
import pandas as pd
from loguru import logger
from impala.dbapi import connect
from impala.util import as_pandas
from impala.interface import Connection, Cursor
from typing import Literal, Optional, overload, Iterable, Any, Mapping, List


class HiveHook:
    """
    Interact with Apache Impala through impyla.
    """
    conn_type = "hive"
    hook_name = "hive"
    _test_connection_sql = "SELECT 1"

    def __init__(
        self,
        *,
        host: str,
        port: int,
        user: str,
        password: str,
        auth_mechanism: Literal["PLAIN", "LDAP"] | None = "PLAIN",
        schema: Optional[str] = None,
        log_sql: bool = True
    ) -> None:
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.auth_mechanism = auth_mechanism
        self.schema = schema
        self.log_sql = log_sql
        self._connection: Optional[Connection] = None
        self._cursor: Optional[Cursor] = None
        self.log = logger

    @property
    def connection(self) -> Connection:
        if self._connection is None:
            self._connection = self.get_conn()

        return self._connection

    @property
    def cursor(self) -> Cursor:
        if self._cursor is None:
            self._cursor = self.get_conn().cursor()
        return self._cursor

    def get_conn(self) -> Connection:
        """
        Returns a connection to the Impala database.
        """
        return connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            auth_mechanism=self.auth_mechanism,
            database=self.schema,
        )

    def close_conn(self) -> None:
        """
        Close the connection to the Impala database.
        """
        if self.connection is not None:
            self.connection.close()
            self._connection = None

    def get_df(
        self,
        sql: str,
        parameters: Optional[dict] = None
    ) -> pd.DataFrame:
        """
        Execute the sql and returns a dataframe.

        :param sql: the sql statement to be executed (str) or a list of sql statements to execute
        :param parameters: The parameters to render the SQL query with.
        """
        return as_pandas(self.cursor)

    def get_first(
        self,
        sql: str | list[str],
        parameters: Iterable | Mapping[str, Any] | None = None
    ) -> Any:
        """
        Execute the sql and return the first resulting row.

        :param sql: the sql statement to be executed (str) or a list of sql statements to execute
        :param parameters: The parameters to render the SQL query with.
        """
        if self.log_sql:
            self.log.info(f"Executing SQL: \n{sql}")

        self.cursor.execute(sql, parameters)
        return self.cursor.fetchone()

    def get_records_from_sql(
        self,
        sql: str,
        parameters: Optional[dict] = None,
        size: int | None = None,
    ):
        """
        Execute the sql and return a set of records.

        :param sql: the sql statement to be executed (str) or a list of sql statements to execute
        :param parameters: The parameters to render the SQL query with.
        :param size:
        """
        self.cursor.fetchmany()
        return self.cursor.fetchall()

    def get_records_from_table(
        self,
        table: str,
        columns: Optional[List[str]] = None,
        database: Optional[str] = None,
    ) -> pd.DataFrame:
        """
        Return a set of records from the table with specified columns.
        """
        if columns is None:
            columns = "*"
        else:
            columns = "\n  , ".join(columns)

        if table.find(".") == -1:
            table = f"{database}.{table}" if database else table

        sql = f"SELECT\n\t {columns} \nFROM {table}"

        if self.log_sql:
            self.log.info(f"\nExecuting SQL: \n{sql}")

        self.cursor.execute(sql)
        return as_pandas(self.cursor)

    @staticmethod
    def strip_sql_string(sql: str) -> str:
        return sql.strip().rstrip(";")

    @staticmethod
    def split_sql_string(sql: str, strip_semicolon: bool = True) -> list[str]:
        """
        Split string into multiple SQL expressions.

        :param sql: SQL string potentially consisting of multiple expressions
        :param strip_semicolon: whether to strip semicolon from SQL string
        :return: list of individual expressions
        """
        splits = sqlparse.split(
            sql=sqlparse.format(sql, strip_comments=True),
            strip_semicolon=strip_semicolon,
        )
        return [s for s in splits if s]

    @overload
    def run(
        self,
        sql: str | Iterable[str],
        parameters: Iterable | Mapping[str, Any] | None = ...,
        split_statements: bool = ...,
        return_last: bool = ...,
    ) -> None: ...

    @overload
    def run(
        self,
        sql: str | Iterable[str],
        parameters: Iterable | Mapping[str, Any] | None = ...,
        split_statements: bool = ...,
        return_last: bool = ...,
    ) -> tuple | list[tuple] | list[list[tuple] | tuple] | None: ...

    def run(
        self,
        sql: str | Iterable[str],
        parameters: Iterable | Mapping[str, Any] | None = None,
        split_statements: bool = True,
        return_last: bool = True,
    ) -> tuple | list[tuple] | list[list[tuple] | tuple] | None:
        """
        Run a command or a list of commands.

        Pass a list of SQL statements to the sql parameter to g0et them to
        execute sequentially.

        The method will return either single query results (typically list of rows) or list of those results
        where each element in the list are results of one of the queries (typically list of list of rows :D)

        For compatibility reasons, the behaviour of the DBAPIHook is somewhat confusing.
        In some cases, when multiple queries are run, the return value will be an iterable (list) of results
        -- one for each query. However, in other cases, when single query is run, the return value will
        be the result of that single query without wrapping the results in a list.

        The cases when single query results are returned without wrapping them in a list are as follows:

        a) sql is string and ``return_last`` is True (regardless what ``split_statements`` value is)
        b) sql is string and ``split_statements`` is False

        In all other cases, the results are wrapped in a list, even if there is only one statement to process.
        In particular, the return value will be a list of query results in the following circumstances:

        a) when ``sql`` is an iterable of string statements (regardless what ``return_last`` value is)
        b) when ``sql`` is string, ``split_statements`` is True and ``return_last`` is False

        After ``run`` is called, you may access the following properties on the hook object:

        * ``descriptions``: an array of cursor descriptions. If ``return_last`` is True, this will be
          a one-element array containing the cursor ``description`` for the last statement.
          Otherwise, it will contain the cursor description for each statement executed.
        * ``last_description``: the description for the last statement executed

        Note that query result will ONLY be actually returned when a handler is provided; if
        ``handler`` is None, this method will return None.

        Handler is a way to process the rows from cursor (Iterator) into a value that is suitable to be
        returned to XCom and generally fit in memory.

        You can use pre-defined handles (``fetch_all_handler``, ``fetch_one_handler``) or implement your
        own handler.

        :param sql: the sql statement to be executed (str) or a list of sql statements to execute
        :param parameters: The parameters to render the SQL query with.
        :param split_statements: Whether to split a single SQL string into statements and run separately
        :param return_last: Whether to return result for only last statement or for all after split
        :return: if handler provided, returns query results (may be list of results depending on params)
        """

    def _run_command(self, sql: str, parameters: Optional[dict] = None):
        """Run a statement using an already open cursor."""
        if self.log_sql:
            self.log.info("Running statement: %s, parameters: %s", sql, parameters)

        if parameters:
            self.cursor.execute(sql, parameters)
        else:
            self.cursor.execute(sql)

        # According to PEP 249, this is -1 when query result is not applicable.
        if self.cursor.rowcount() >= 0:
            self.log.info("Rows affected: %s", self.cursor.rowcount)

    def test_connection(self) -> tuple[bool, str]:
        """
        Test the connection use special query.
        """
        status, message = False, ""
        try:
            if self.get_first(self._test_connection_sql):
                status = True
                message = "Connection successfully tested"
        except Exception as e:
            status = False
            message = str(e)

        return status, message

    def insert_records(
        self,
        table,
        records,
        target_fields=None,
        replace=False,
        *,
        executemany=False,
        fast_executemany=False,
        **kwargs,
    ):
        """
        Insert a collection of tuples into a table.

        Rows are inserted in chunks, each chunk (of size ``commit_every``) is
        done in a new transaction.

        :param table: Name of the target table
        :param records: The rows to insert into the table
        :param target_fields: The names of the columns to fill in the table
        :param replace: Whether to replace instead of insert
        :param executemany: If True, all rows are inserted at once in
            chunks defined by the commit_every parameter. This only works if all rows
            have same number of column names, but leads to better performance.
        :param fast_executemany: If True, the `fast_executemany` parameter will be set on the
            cursor used by `executemany` which leads to better performance, if supported by driver.
        :param autocommit: What to set the connection's autocommit setting to
            before executing the query.
        """

    def create_database(
        self,
        database_name,
    ) -> None:
        """
        Create a database.

        :param database_name: Name of the database to create
        """
        create_db_sql = f"CREATE DATABASE IF NOT EXISTS {database_name}"
        self.run(create_db_sql)

    def drop_database(
        self,
        database_name,
    ) -> None:
        """
        Drop a database.
        """
        drop_db_sql = f"DROP DATABASE IF EXISTS {database_name}"
        self.run(drop_db_sql)

    def load_df(self):
        """

        """

    def load_file(self):
        """

        """

    def get_databases(self, pattern: str = '*'):
        """

        """

    def get_tables(self, pattern: str = '*'):
        """

        """

    def get_partitions(self):
        """

        """

    def add_partition(self):
        """

        """

    def drop_partition(self):
        """

        """

    def table_exists(self, table_name: str):
        """

        """

