from sqlalchemy import MetaData, Table, Column, Integer, String, DateTime
from datetime import datetime
from pytz import timezone

from .base import Base


class Command_counts(Base):
    __tablename__ = "command_counts"

    id = Column(Integer, primary_key=True)
    server = Column(String(255))
    command = Column(String(255))
    created_at = Column(DateTime(), default=datetime.now(timezone("Asia/Seoul")))

    def __init__(self, server, command):
        self.server = server
        self.command = command

    def __repr__(self):
        return "<command_counts %s %s %s>" % (
            self.server,
            self.command,
            self.created_at,
        )
