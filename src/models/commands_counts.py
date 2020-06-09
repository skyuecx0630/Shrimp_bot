from sqlalchemy import MetaData, Table, Column, Integer, String

from .base import Base


class Command_counts(Base):
    __tablename__ = "command_counts"

    id = Column(Integer, primary_key=True)
    server = Column(String(255))
    command = Column(String(255))
    counts = Column(Integer)

    def __init__(self, command, counts):
        self.command = command
        self.counts = counts

    def __repr__(self):
        return "<command_counts %s %s>" % (self.command, self.counts)
