import time
from os import path
import allure
from sshtunnel import SSHTunnelForwarder
from sqlalchemy import create_engine, exc
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker
from log.app import Logger


class DBConnect:

    def __init__(self, host: str, db_name="rtknm", username="rtknm", password="rtknm", port="5432",
                 use_ssh=False, ssh_port=22,
                 ssh_username="centos", ssh_pkey=None, drivername="postgresql", echo=False,
                 autocommit=False, logger=None, retry=2):
        """
        object for connect with database with sqlalchemy session
        :param host: db host
        :param port: db port
        :param db_name: db name
        :param username: user for db
        :param password: password for db
        :param use_ssh: True if need ssh tunnel
        :param ssh_port: str, required if use ssh, port for ssh connect
        :param ssh_username: str, required if use ssh, user for ssh connect
        :param ssh_pkey: str, required if use ssh, path to ssh key
        :param drivername: name of db driver
        :param echo: stdout sqlalchemy forming and sending requests
        :param autocommit: autocommit transactions
        :param logger: logger object
        :param retry: queries retry if lose connect
        """
        self.retry = retry
        self.autocommit = autocommit
        if logger:
            self.logger = logger
        else:
            self.logger = Logger(service_name='db_client')

        if use_ssh:
            assert ssh_port and ssh_username and ssh_pkey, \
                "for using ssh, you need to set: ssh_port, ssh_username, ssh_pkey"
            assert path.exists(ssh_pkey), \
                "for using ssh, you need to add ssh key to project root"

            server = SSHTunnelForwarder(
                (host, int(ssh_port)),
                ssh_username=ssh_username,
                ssh_pkey=ssh_pkey,
                remote_bind_address=('0.0.0.0', int(port)),
            )
            server.daemon_forward_servers = True
            server.daemon_transport = True
            server.start()

            host = "127.0.0.1"
            port = str(server.local_bind_port)

        db_url = URL(drivername=drivername, username=username, password=password,
                     host=host, port=port, database=db_name)
        pgsql = create_engine(db_url,
                              echo=echo,
                              pool_recycle=300,
                              pool_pre_ping=True,
                              )
        self.session = sessionmaker(pgsql, autocommit=self.autocommit)()

    def _get_cursor(self, sql: str, rowcount_return=False) -> iter:
        """
        inner def for execute transaction
        :param sql: sql query
        :param rowcount_return: True for return rowcount instead of cursor
        :return: cursor for db
        """
        self.logger.info(f"SQL:\n{sql}")
        cursor = None
        try:
            retry = self.retry + 1
            while retry:
                retry -= 1
                try:
                    cursor = self.session.execute(sql)
                    if not self.autocommit:
                        self.session.commit()
                    if rowcount_return:
                        cursor = cursor.rowcount
                except exc.DBAPIError as e:
                    self.logger.error("Failed to execute query: {}\nquery: {}".format(e, sql))
                    self.session.rollback()
                else:
                    break
        except Exception as e:
            self.logger.error("Failed to execute query: {}\nquery: {}".format(e, sql))
            self.session.rollback()
        return cursor

    def execute_sql(self, sql: str) -> int:
        """
        simple execute sql command without results (delete, update)
        :param sql: sql query
        :return: count of matched rows
        """
        rowcount = self._get_cursor(sql, rowcount_return=True)
        if rowcount == 0:
            self.logger.warning("0 rows is matched to sql: {}".format(sql))
        return rowcount

    def get_one_result(self, sql: str) -> any:
        """
        simple select one field from one row
        :param sql: sql query
        :return: field from db
        """
        cursor = self._get_cursor(sql)
        result = None
        if cursor.rowcount != 0:
            result = next(cursor)[0]
            cursor.close()
        return result

    def get_list_result(self, sql: str) -> list:
        """
        select with result list
        :param sql: sql query
        :return: list of lists with db rows
        """
        cursor = self._get_cursor(sql)
        result = list(list(row) for row in cursor) if cursor else []
        return result

    def get_dict_result(self, sql: str) -> list:
        """
        select with result dict
        :param sql: sql query
        :return: list of dicts with db rows
        """
        cursor = self._get_cursor(sql)
        result = [dict(row) for row in cursor] if cursor else []
        return result
