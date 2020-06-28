from sqlalchemy import MetaData, Table, Column, Integer, String

from .base import Base


class Custom_commands(Base):
    __tablename__ = "custom_commands"

    id = Column(Integer, primary_key=True)
    server = Column(String(50))
    author = Column(String(50))
    command = Column(String(255))
    output = Column(String(255))

    def __init__(self, server, author, command, output):
        self.server = server
        self.author = author
        self.command = command
        self.output = output

    def __repr__(self):
        return "<custom_commands %s %s %s %s>" % (
            self.server,
            self.author,
            self.command,
            self.output,
        )
