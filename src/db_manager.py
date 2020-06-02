import configparser
from sqlalchemy import create_engine 
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from os.path import join, exists
from models import Custom_commands

from const import Settings


class DBManager:
    def __init__(self):
        engine = create_engine(Settings.database)

        from models import Base
        Base.metadata.create_all(engine)

        session = sessionmaker()
        session.configure(bind=engine)
        self.session = session()


    def insert_row(self, data):
        self.session.add(data)
        self.session.commit()
        
    def search_row(self, table, column, data):
        key = getattr(table, column)
        query = self.session.query(table).filter(key == (data))
        return query.all()

    def delete_row(self, data):
        self.session.delete(data)
        self.session.commit()


if __name__ == '__main__':
    m = DBManager()
    data = Custom_commands(5, 'com', 'out')
    # m.insert_row(data)
    print(m.search_row(Custom_commands, 'command', 's'))