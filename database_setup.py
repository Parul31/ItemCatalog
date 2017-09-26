import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class User(Base):
        __tablename__ = 'user'

        id = Column(Integer, primary_key=True)
        name = Column(String(250), nullable=False)
        email = Column(String(250), nullable=False)
        picture = Column(String(250))


class FamousCities(Base):
        __tablename__ = 'famous_cities'

        id = Column(Integer, primary_key=True)
        name = Column(String(250), nullable=False)

        @property
        def serialize(self):
                """Return object data in easily serializeable format"""
                return {
                        'name': self.name,
                        'id': self.id,
                        }


class FamousPlaces(Base):
        __tablename__ = 'famous_places'

        name = Column(String(200), nullable=False)
        id = Column(Integer, primary_key=True)
        description = Column(String(500))
        address = Column(String(250))
        famous_city_id = Column(Integer, ForeignKey('famous_cities.id'))
        famous_city = relationship(FamousCities, cascade="all, delete-orphan")
        user_id = Column(Integer, ForeignKey('user.id'))
        user = relationship(User)

        @property
        def serialize(self):
                """Return object data in easily serializeable format"""
                return {
                        'name': self.name,
                        'description': self.description,
                        'id': self.id,
                        'address': self.address
                        }


engine = create_engine('sqlite:///famousplaces.db')

Base.metadata.create_all(engine)
