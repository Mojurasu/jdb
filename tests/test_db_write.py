import pytest
import jdb
import json
import secrets


def json_check_key(key, value):
    with open('tests/data/test_db_write.db', 'r') as f:
        j = json.load(f)
        return j[key] == value


@pytest.fixture
def setup_db():
    db:  jdb.Database = jdb.Database('tests/data/test_db_write')
    yield db
    db.clear()
    db.save()
    # db.delete()


def random_values():
    return secrets.token_urlsafe(10), secrets.token_urlsafe(10)


@pytest.fixture
def random_vals():
    return random_values()


def test_set(setup_db, random_vals):
    db: jdb.Database
    with setup_db as db:
        db.set(*random_vals)

    assert json_check_key(*random_vals)


def test_set_item(setup_db, random_vals):
    db: jdb.Database
    with setup_db as db:
        db[random_vals[0]] = random_vals[1]
    assert json_check_key(*random_vals)


def test_clear(setup_db):
    db: jdb.Database
    with setup_db as db:
        for i in range(10):
            vals = random_values()
            db.set(*vals)
        assert len(db.db_data) == 11  # 10 + 1 for the version
        db.clear()
    assert len(db.db_data) == 1
