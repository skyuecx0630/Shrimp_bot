from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base, Custom_commands

from const import Settings


class DBManager:
    def __init__(self):
        self.engine = create_engine(Settings.database)

        Base.metadata.create_all(self.engine)

    def insert_row(self, data):
        with Session(self.engine) as session:
            session.add(data)
            session.commit()

    def search_row(self, table, column, data):
        key = getattr(table, column)
        with Session(self.engine) as session:
            query = session.query(table).filter(key == (data))
        return query.all()

    def delete_row(self, data):
        with Session(self.engine) as session:
            session.delete(data)
            session.commit()


class Session:
    def __init__(self, engine):
        self.engine = engine
        self.session = None

    def __enter__(self):
        self.session = sessionmaker(bind=self.engine)()

        return self.session

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()


if __name__ == "__main__":
    m = DBManager()
    data = Custom_commands(5, "com", "out")
    # m.insert_row(data)
    print(m.search_row(Custom_commands, "command", "s"))
