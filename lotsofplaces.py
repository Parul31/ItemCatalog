# -*- coding: utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, FamousCities, FamousPlaces

engine = create_engine('sqlite:///famousplaces.db')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()

city1 = FamousCities(name='Mumbai')

session.add(city1)
session.commit()

city2 = FamousCities(name='Bengaluru')

session.add(city2)
session.commit()


city3 = FamousCities(name='Delhi')

session.add(city3)
session.commit()


city4 = FamousCities(name='Chandigarh')

session.add(city4)
session.commit()



print "added famous cities!"
