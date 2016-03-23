"""Define models for learning journalapp."""
from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
    DateTime,
    String,
)

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
)

from pyramid.security import (
    Allow,
    Everyone,
    Authenticated,
    )

from zope.sqlalchemy import ZopeTransactionExtension

import datetime

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()

class Entry(Base):
    """Model Entry."""

    __tablename__ = "entries"
    id = Column(Integer, primary_key=True)
    title = Column(String(128), unique=True)
    text = Column(Text)
    created = Column(DateTime, default=datetime.datetime.utcnow)


class DefaultRoot(object):
    """Default acl modle."""
    __acl__ = [
        (Allow, Everyone, 'view'),
        (Allow, Authenticated, 'add'),
        (Allow, Authenticated, 'edit')
        ]

    def __init__(self, request):
        pass

