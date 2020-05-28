import configparser
from sqlalchemy import create_engine 
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from os.path import join, exists
from models import Custom_commands

from const import Databases


class DBManager:
    def __init__(self):
        engine = create_engine(Databases.local)

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

if __name__ == '__main__':
    m = DBManager()
    data = Custom_commands(5, 'com', 'out')
    # m.insert_row(data)
    print(m.search_row(Custom_commands, 'command', 's'))