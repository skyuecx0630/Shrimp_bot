from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData, Table, Column, Integer, String

Base = declarative_base()

class Custom_commands(Base):
    __tablename__ = 'custom_commands'

    id      = Column(Integer, primary_key=True)
    server  = Column(String(50))
    command = Column(String(255))
    output  = Column(String(255))

    def __init__(self, server, command, output):
        self.server = server
        self.command = command
        self.output = output

    def __repr__(self):
        return '<Custom_commands %s %s %s>' % (self.server, self.command, self.output)
