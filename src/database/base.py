import configparser
from contextlib import contextmanager
from enum import Enum, auto

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


def load_engine(config_path: str):
    """
    Create a sql connection based on config from defined ini file
    :param config_path: str, path to ini file
    :return: slqalchemy engine
    """
    config = configparser.ConfigParser()
    config.read(config_path)

    db_to_use = config['DEFAULT']['UseDatabase']
    db_config = config[db_to_use]

    db_type = db_config['DatabaseType']
    username = db_config['Username']
    password = db_config['Password']
    address = db_config['Address']
    port = db_config['Port']

    conn_string = f'{db_type}://{username}:{password}@{address}:{port}/{username}'

    return create_engine(conn_string)


engine = load_engine('./database/db.ini')
Session = sessionmaker(bind=engine)
Base = declarative_base()


class SessionMode(Enum):
    """Enum for use with session_scope to enable/disable .commit() to db"""
    READ = auto()
    WRITE = auto()


@contextmanager
def session_scope(mode: SessionMode):
    session = Session()
    try:
        yield session
        if mode == SessionMode.WRITE:
            session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()




