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

city5 = FamousCities(name='Kolkata')

session.add(city5)
session.commit()

city6 = FamousCities(name='Agra')

session.add(city6)
session.commit()

city7 = FamousCities(name='Chennai')

session.add(city7)
session.commit()

city8 = FamousCities(name='Varanasi')

session.add(city8)
session.commit()

city9 = FamousCities(name='Amritsar')

session.add(city9)
session.commit()

city10 = FamousCities(name='Pondicherry')

session.add(city10)
session.commit()

print "added famous cities!"
