import os

from sqlalchemy import *
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_fdw import ForeignTable, ForeignDataWrapper
from sqlalchemy_utils.functions import create_database
from sqlalchemy_utils.functions import drop_database
from sqlalchemy_utils.functions import database_exists

DB_URI = 'pgfdw://vagrant@localhost:5432/pooshield_test'

def sqlalchemy_engine(echo=False):
    return create_engine(DB_URI, echo=echo, convert_unicode=True)

def sqlalchemy_session(engine=None):
    if not engine:
        engine = sqlalchemy_engine()
    return scoped_session(
        sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=engine
        )
    )

Base = declarative_base()

class MaxEmail(Base):
    __table__ = ForeignTable("gmail", Base.metadata,
        Column('Message-ID', String, primary_key=True),
        Column('From', String),
        Column('Subject', String),
        Column('payload', String),
        Column('flags', ARRAY(String)),
        Column('To', String),
        pgfdw_server='multicorn_email',
        pgfdw_options={ 
            'host': 'imap.gmail.com',
            'port': '993',
            'payload_column': 'payload',
            'flags_column': 'flags',
            'ssl': 'True',
            'login': os.environ.get('TEST_GMAIL_EMAIL', ''),
            'password': os.environ.get('TEST_GMAIL_PASS', '')
        },
        keep_existing=False
    )


def create_db(engine):
    os.system("createdb pooshield_test")
    os.system('sudo -u postgres psql pooshield_test -c "grant usage on foreign data wrapper multicorn to vagrant"')

    engine = sqlalchemy_engine(echo=True)
    Base.metadata.bind = engine
    fdw = ForeignDataWrapper(
        "multicorn_email", 
        "multicorn", 
        metadata=Base.metadata, 
        options={"wrapper": "emailfdw.EmailFdw"}
    )
    fdw.create()

    Base.metadata.create_all(bind=engine)

def drop_db(engine):
    engine.dispose()
    #os.system('psql pooshield_test -c "drop server multicorn_email cascade"')
    os.system('dropdb pooshield_test')
