from sqlalchemy import MetaData, Table, Column, Integer, String

from .base import Base


class Banned_words(Base):
    __tablename__ = "banned_words"

    id = Column(Integer, primary_key=True)
    server = Column(String(50))
    author = Column(String(50))
    words = Column(String(255))

    def __init__(self, server, author, words):
        self.server = server
        self.author = author
        self.words = words

    def __repr__(self):
        return "<banned_words %s %s %s>" % (self.server, self.author, self.words)
