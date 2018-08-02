#!/usr/bin/python
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine

# check if db exists
engine = create_engine('sqlite:///db.sqlite', echo=True)
Base = declarative_base()
Base.metadata.bind = engine



class TextSource(Base):
    __tablename__ = 'text_sources'
    id = Column(Integer, primary_key=True)
    document = Column(String)
    article = Column(String)

    def __repr__(self):
        return "<TextSource(id='%s', document='%s', article='%s')>" % (self.id, self.document, self.article)


def assign(document, article):
    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session()
    text_source = TextSource(document=document, article=article)
    session.add(text_source)
    session.flush()
    session.refresh(text_source)
    # refresh updates given object in the session with its state in the DB
    # (and can also only refresh certain attributes - search for documentation)
    session.commit()
    return text_source.id


def retrieve(text_source_id):
    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session()
    query = session.query(TextSource).filter(TextSource.id == text_source_id)
    _row = query.first()
    return _row.document, _row.article


# create tables if needed
if not engine.dialect.has_table(engine, 'text_sources'):
    Base.metadata.create_all()
