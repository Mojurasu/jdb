"""A simple json based Database.

Todo:
    * Maybe move Errors out of this file
"""

import json
import os
import logging

__version__ = '0.2.1'

logging.getLogger('jdb')


class Database:
    """Basic Class with get and set functions and context manager support."""

    db_data: dict = None
    _init_data = {'__jdbinfo__': {'version': __version__}}

    def __init__(self, name):
        """Create or load the database.

        Create a new file if it doesnt exist yet. The file will be saved
         relative to the current working directory.

        Args:
            name: Name of the database. Can be a absolute path.
        """
        self.name = name
        # Windows paths have backslashes
        path = os.path.abspath(name).replace('\\', '/')
        self.db_path = path + '.db'

        os.makedirs('/'.join(self.db_path.split('/')[:-1]), exist_ok=True)
        if not os.path.exists(self.db_path):
            self.db_data = self._init_data
            with open(self.db_path, 'w', encoding='utf-8') as f:
                json.dump(self._init_data, f)
        elif os.path.isdir(self.db_path):
            raise PathIsDirectoryError('The specified path is a directory.')
        elif os.path.exists(self.db_path) and os.path.isfile(self.db_path):
            with open(self.db_path, 'r', encoding='utf-8') as f:
                self.db_data = json.load(f)

    def __enter__(self):
        """Return self when using a context manager.

        Returns:
            Database

        """
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Save database when the context manager is closed.

        Args:
            exc_type:
            exc_val:
            exc_tb:

        Returns:
            None

        """
        self.save()

    def __getitem__(self, item):
        """Allow db access through key access Syntax..

        Examples:
            >>> j = Database('test')
            >>> j.set('example', 'value')
            >>> print(j['example'])
            value

        Args:
            item: The name of the key.

        Returns:
            Value of the key.

        """
        return self.get(item)

    def __setitem__(self, key, value):
        """Allow db access through key access Syntax..

        Examples:
            >>> j = Database('test')
            >>> j['example'] = 'value'
            >>> print(j['example'])
            value

        Args:
            key: The name of the key.
            key: The value of the key.

        Returns:
            None

        """
        return self.set(key, value)

    def __delitem__(self, key):
        """Allow db access through key access Syntax..

        Examples:
            >>> j = Database('test')
            >>> j.set('example', 'value')
            >>> del j['example']
            >>> print(j['example'])
            None

        Args:
            key: The name of the key.

        Returns:
            None

        """
        return self.remove(key)

    def __contains__(self, item):
        """Allow checking if keys are in the db using the `in` keyword.

        Examples:
            >>> j = Database('test')
            >>> j.set('example', 'value')
            >>> print('example' in j)
            True

        Args:
            item: The name of the key.

        Returns:
            Value of the key.

        """
        return item in self.db_data

    def remove(self, key):
        """Remove the key if it exists.

        Args:
            key: The name of the key.

        Returns:
            None

        """
        try:
            del self.db_data[key]
        except KeyError:
            pass

    def get(self, key):
        """Get the specified key.

        Args:
            key: The name of the key in the db

        Returns:
            The value of `key` if it exists, else `None`

        """
        try:
            return self.db_data[key]
        except KeyError:
            return None

    def get_key_by_value(self, value):
        """Get keys that have a certain value.

        Args:
            value: The value the keys need to have.

        Returns:
            A list with the keys, empty list if no keys were found.

        """
        return [k for k, v in self.db_data.items() if value in v]

    def set(self, key, value):
        """Set the specified key to the specified value.

         Overwrite if it exists.

        Args:
            key: The name of the key.
            value: The value of the key.

        Returns:
            None

        """
        self.db_data[key] = value

    def save(self):
        """Save the database to a file.

        This method isnt needed if you use the db with a context manager.

        Returns:
            None

        """
        if os.path.exists(self.db_path) and os.path.isfile(self.db_path):
            with open(self.db_path, 'w', encoding='utf-8') as f:
                json.dump(self.db_data, f)

    def clear(self):
        """Clear the entire database.

        Returns:
            None

        """
        self.db_data = self._init_data


class PathIsDirectoryError(Exception):
    """Raised when the specified database name is a directory."""

    pass
