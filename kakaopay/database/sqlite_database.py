
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session


class SqliteDataBase:
    db_entity = declarative_base()
    _db_session = None

    @classmethod
    def open(cls, db_path: str):
        db_path = 'sqlite:///' + db_path
        engine = create_engine(db_path, echo=True)

        cls._db_session = sessionmaker(bind=engine)
        cls.db_entity.metadata.create_all(engine)

    @classmethod
    def create_session(cls):
        return cls._db_session()

    @classmethod
    def close(cls, session: Session):
        session.close()
