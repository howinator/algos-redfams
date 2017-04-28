from typing import List, Dict, Union, Any, Tuple
import os.path
import yaml


import psycopg2 as pg
import psycopg2.extras as pgextra


class SQLWrapper(object):
    def __init__(self, connection_vars: Dict[str, Union[str, int]]) -> None:
        # No sensible default db_host, so just fail if it's undefined
        try:
            self._host = connection_vars['db_host']
        except KeyError as e:
            print('The database\'s host must be defined ' + str(e))
            raise e
        self._dbname = connection_vars.get('db_name', 'postgres')
        self._user = connection_vars.get('db_user', 'postgres')
        self._pass = connection_vars.get('db_pass', 'postgres')
        self._port = connection_vars.get('db_port', 5432)

    def __enter__(self) -> Any:
        self.con = pg.connect(dbname=self._dbname, host=self._host, password=self._pass, port=self._port,
                              user=self._user)
        return self

    def __exit__(self, *args) -> None:
        self.con.close()

    def add_subreddits(self, subreddits: List[str]) -> None:
        """
        Adds subreddits to database
        
        :param subreddits: List of subreddit names
        :return: None
        """
        tuples = [(name,) for name in subreddits]
        with self.con.cursor() as cur:
            # If we try to add a duplciate, just skip it
            pgextra.execute_values(cur, "INSERT INTO subreddits (name) VALUES %s ON CONFLICT (name) DO NOTHING;",
                                   tuples)
            self.con.commit()

    def add_comments(self, usernames: List[str], subreddits: List[str]) -> None:
        """
        Adds username, subreddit pairs to the database
        
        :param usernames: List of usernames
        :param subreddits: List of subreddit names
        :return: None
        """
        tuples = zip(usernames, subreddits)
        with self.con.cursor() as cur:
            pgextra.execute_values(
                cur,
                "INSERT INTO comments (username, subreddit) VALUES %s ON CONFLICT (username, subreddit) DO NOTHING;",
                tuples
            )
            self.con.commit()

    def get_subreddits(self) -> List[Tuple[str]]:

        with self.con.cursor() as cur:
            cur.execute("SELECT DISTINCT name FROM subreddits ORDER BY name;")
            results = cur.fetchall()

        return results

    def get_user_sub_pairs(self) -> List[Tuple[str]]:
        """
        Simply returns unique (username, subreddit) pairs sorted by username
        """

        with self.con.cursor() as cur:
            query="SELECT DISTINCT username, subreddit FROM comments GROUP BY username, subreddit ORDER BY username;"
            cur.execute(query)
            results = cur.fetchall()

        return results

    def get_users(self, start: int = None, stop: int = None) -> List[str]:
        """
        Gets users with optional start and stop positions.
        If start and stop are not provided, all users are fetched
        
        :param start: first user id to fetch
        :param stop: last user id to fetch
        :return: returns list of usernames
        """
        if start is None and stop is None:
            query_string = "SELECT username FROM users"
            params_tuple = ()
        else:
            query_string = "SELECT username FROM USERS WHERE id >= %s AND id <= %s"
            params_tuple = (start, stop)

        with self.con.cursor() as cur:
            cur.execute(query_string, params_tuple)
            user_tuple_list = cur.fetchall()
            user_list = [t[0] for t in user_tuple_list]
        return user_list

    def add_users(self, usernames: List[str]) -> List[str]:
        """
        Add users to database and return users actually added to database (non-duplicates)
        
        :param usernames: List of usernames
        :return: List of usernames added to database
        """
        with self.con.cursor() as cur:
            cur.execute("SELECT id FROM users ORDER BY id DESC LIMIT 1")
            try:
                prev_last_id = cur.fetchone()[0]
            # Catch the case where no users have been added to the database yet
            except TypeError:
                prev_last_id = -1
        tuples = [(name,) for name in usernames]
        with self.con.cursor() as cur:
            pgextra.execute_values(cur, "INSERT INTO users (username) VALUES  %s ON CONFLICT (username) DO NOTHING;",
                                   tuples)
            self.con.commit()
        with self.con.cursor() as cur:
            cur.execute("SELECT * FROM users WHERE id > %s", (prev_last_id,))
            results = cur.fetchall()
            added_users = [tup[1] for tup in results]
        return added_users


class ConfigHelper(object):
    def __init__(self, env):
        self._env = env
        vars_dir_path = self._get_vars_dir_path()
        self._env_config_file_path = self._form_env_config_path(vars_dir_path)
        creds_file_path = self._form_creds_path(vars_dir_path)
        self._creds = self._load_file(creds_file_path)

    @property
    def config(self):
        db_password_key = "{env}_pg_pass".format(env=self._env)

        config_vars = self._load_file(self._env_config_file_path)

        config_vars['db_pass'] = self._creds[db_password_key]
        return config_vars

    @property
    def creds(self):
        return self._creds

    @staticmethod
    def _load_file(path: str) -> Dict[str, str]:
        file_contents = {}
        with open(path, 'r') as f:
            try:
                file_contents = yaml.load(f)
            except yaml.YAMLError as e:
                print(str(e))
                raise e
        return file_contents

    @staticmethod
    def _get_vars_dir_path() -> str:
        sqlwrapper_file_path = __file__
        return os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(sqlwrapper_file_path))), 'infra', 'vars')

    def _form_env_config_path(self, vars_dir: str) -> str:
        env_config_basename = "{env}.yml".format(env=self._env)
        return os.path.join(vars_dir, env_config_basename)

    @staticmethod
    def _form_creds_path(vars_dir: str) -> str:
        creds_basename = 'creds.yml'
        return os.path.join(vars_dir, creds_basename)
