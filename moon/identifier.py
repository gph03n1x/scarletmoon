#!/usr/bin/python
from contextlib import contextmanager
import datetime
import hashlib
import settings
import sqlalchemy.exc
from sqlalchemy import Column, Integer, String, create_engine, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

DB_ECHO = settings.DB_ECHO
# check if db exists
engine = create_engine('sqlite:///db.sqlite', echo=DB_ECHO)
Base = declarative_base()
Base.metadata.bind = engine


@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


class TextSource(Base):
    __tablename__ = 'text_sources'
    id = Column(Integer, primary_key=True)
    document = Column(String)
    article = Column(String)
    url = Column(String)
    hash = Column(String, unique=True)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)
    modified_date = Column(DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return "<TextSource(id='%s', document='%s', article='%s')>" % (self.id, self.document, self.article)


def get_hash(document, article):
    m = hashlib.sha256()
    m.update(bytes(document, encoding='utf8'))
    m.update(bytes(article, encoding='utf8'))
    return m.hexdigest()


def assign(document, article, url=""):
    doc_hash = get_hash(document, article)

    with session_scope() as session:
        try:
            text_source = TextSource(document=document, article=article, url=url, hash=doc_hash)
            session.add(text_source)
            session.commit()
        except sqlalchemy.exc.IntegrityError:
            # update the modified time.
            session.rollback()
            query = session.query(TextSource).filter(TextSource.hash == doc_hash)
            _row = query.first()
            _row.modified_date = datetime.datetime.utcnow()
            session.merge(_row)
            session.commit()

    return doc_hash


def retrieve_by_hash(doc_hash):
    with session_scope() as session:
        query = session.query(TextSource).filter(TextSource.hash == doc_hash)
        _row = query.first()
        return {'id': _row.id, 'document': _row.document, 'article': _row.article, 'hash': _row.hash, 'url': _row.url,
                'created': str(_row.created_date), 'modified': str(_row.modified_date)}


# create tables if needed
if not engine.dialect.has_table(engine, 'text_sources'):
    Base.metadata.create_all()
