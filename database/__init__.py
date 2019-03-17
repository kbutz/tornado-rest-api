from sqlalchemy import create_engine, Column, String, Integer, Numeric, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# NOTE: echo logs sql statements and should be disabled in production
engine = create_engine('mysql+pymysql://root:password@192.168.1.6:3306/tornado', echo=True)

Session = sessionmaker(bind=engine)

Base = declarative_base()


def init_models():
    Base.metadata.create_all(engine)


class Product(Base):
    __tablename__ = 'products'
    id=Column(Integer, primary_key=True)
    title=Column('title', String(32))
    in_stock=Column('in_stock', Boolean)
    quantity=Column('quantity', Integer)
    price=Column('price', Numeric)

    def add(self):
        session = Session()
        session.add(self)
        session.commit()
        session.close()

