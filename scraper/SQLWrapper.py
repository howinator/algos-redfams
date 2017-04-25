import psycopg2 as pg


class SQLWrapper(object):

    def __init__(self, connection_vars):
        # No sensible default db_host, so just fail if it's undefined
        try:
            self._host = connection_vars['db_host']
        except KeyError as e:
            print('The database\'s host must be defined ' + e)
            raise e
        self._dbname = connection_vars.get('db_name', 'postgres')
        self._user = connection_vars.get('db_user', 'postgres')
        self._pass = connection_vars.get('db_pass', 'postgres')
        self._port = connection_vars.get('db_port', 5432)

    def __enter__(self):
        self.con = pg.connect(dbname=self._dbname, host=self._host, password=self._pass, port=self._port)
        self.cur = self.con.cursor()
        return self

    def __exit__(self, *args):
        self.con.close()

    def add
