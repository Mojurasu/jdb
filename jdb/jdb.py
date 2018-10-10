import json
import os
import logging

__version__ = 0.1

logging.getLogger('jdb')


class Database:
    db_data: dict = None
    _init_data = {'__jdbinfo__': {'version': 0.1}}

    def __init__(self, name):
        self.name = name
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
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.save()

    def __getitem__(self, item):
        return self.get(item)

    def __setitem__(self, key, value):
        return self.set(key, value)

    def __delitem__(self, key):
        return self.remove(key)

    def get(self, key):
        try:
            return self.db_data[key]
        except KeyError:
            return None

    def get_key_by_value(self, value):
        return [k for k, v in self.db_data.items() if value in v]

    def set(self, key, value):
        self.db_data[key] = value

    def remove(self, key):
        try:
            del self.db_data[key]
        except KeyError:
            pass

    def __contains__(self, item):
        return item in self.db_data

    def save(self):
        if os.path.exists(self.db_path) and os.path.isfile(self.db_path):
            with open(self.db_path, 'w', encoding='utf-8') as f:
                json.dump(self.db_data, f)

    def clear(self):
        self.db_data = self._init_data


class PathIsDirectoryError(Exception):
    """Raised when the specified database name is a directory."""
    pass
