from app import app
from sqlalchemy import *
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import types
import datetime


__all__ = ['db_session', 'Base', 'engine', 'Order']

engine = create_engine(
    app.config['SQLALCHEMY_DATABASE_URI'],
    convert_unicode=True,
    pool_recycle=3600,
)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=True,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()
Base.metadata.create_all(bind=engine)


class Order(Base):
    __tablename__ = 'order'
    id = Column(Integer, primary_key=True)
    date = Column(DateTime, default=datetime.datetime.now())
    name = Column(String(120))
    street = Column(String(120))
    street2 = Column(String(120))
    city = Column(String(120))
    state = Column(String(120))
    zip_code = Column(String(120))
    country = Column(String(120))
    email = Column(String(120))
    username = Column(String(120))
    item = Column(String(120))
    price = Column(Numeric(precision=10, scale=2))
    paid = Column(Boolean, default=False)

    def __unicode__(self):
        return self.id


# Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)
