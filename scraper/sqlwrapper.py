from typing import List, Dict, Union, Any

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
            pgextra.execute_values(cur,
                "INSERT INTO comments (username, subreddit) VALUES %s ON CONFLICT (username, subreddit) DO NOTHING;",
                tuples)
            self.con.commit()

    def get_users(self, start: int =None, stop: int =None) -> List[str]:
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
