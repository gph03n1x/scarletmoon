#!/usr/bin/python
import hashlib

import sqlalchemy.exc
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# check if db exists
engine = create_engine('sqlite:///db.sqlite', echo=True)
Base = declarative_base()
Base.metadata.bind = engine


class TextSource(Base):
    __tablename__ = 'text_sources'
    id = Column(Integer, primary_key=True)
    document = Column(String)
    article = Column(String)
    url = Column(String)
    hash = Column(String, unique=True)

    def __repr__(self):
        return "<TextSource(id='%s', document='%s', article='%s')>" % (self.id, self.document, self.article)


def get_hash(document, article):
    m = hashlib.sha256()
    m.update(bytes(document, encoding='utf8'))
    m.update(bytes(article, encoding='utf8'))
    return m.hexdigest()


def assign(document, article):
    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session()
    doc_hash = get_hash(document, article)
    try:
        text_source = TextSource(document=document, article=article, url="", hash=doc_hash)
        session.add(text_source)
        session.flush()
        session.refresh(text_source)
        # refresh updates given object in the session with its state in the DB
        # (and can also only refresh certain attributes - search for documentation)
        session.commit()
    except sqlalchemy.exc.IntegrityError:
        pass

    return doc_hash


def retrieve_by_hash(doc_hash):
    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session()
    query = session.query(TextSource).filter(TextSource.hash == doc_hash)
    _row = query.first()
    return _row.id, _row.document, _row.article, _row.hash



# create tables if needed
if not engine.dialect.has_table(engine, 'text_sources'):
    Base.metadata.create_all()
