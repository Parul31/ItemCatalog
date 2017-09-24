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

place1 = FamousPlaces(name='Gateway of India',
                      description="The Gateway of India is an arch monument"
                      " built during the 20th century in Bombay, India. The"
                      " monument was erected to commemorate the landing of "
                      "King George V and Queen Mary at Apollo Bunder on "
                      "their visit to India in 1911.", address="Address:"
                      "Apollo Bandar, Colaba, Mumbai, Maharashtra 400001",
                      famous_city=city1)

session.add(place1)
session.commit()

place2 = FamousPlaces(name='Chhatrapati Shivaji Maharaj Vastu Sangrahalaya',
                      description="Chhatrapati Shivaji Maharaj Vastu"
                      " Sangrahalaya, formerly known as the Prince of Wales"
                      " Museum of Western India, is one of the premier art "
                      "and history museums in India. The Museum building, "
                      "a Grade I Heritage building, is a fine example of the"
                      " Indo-Saracenic style of architecture and houses a "
                      "world-class collection of over 60,000 art objects.",
                      address="159-161, Mahatma Gandhi Road, Fort, Mumbai,"
                      " Maharashtra 400032", famous_city=city1)

session.add(place2)
session.commit()

city2 = FamousCities(name='Bengaluru')

session.add(city2)
session.commit()

place1 = FamousPlaces(name='Lal Bagh', description="Lalbagh or Lalbagh "
                      "Botanical Gardens, meaning The Red Garden in English,"
                      " is a well known botanical garden in southern"
                      " Bengaluru, India.", address="Mavalli, "
                      "Bengaluru, Karnataka 560004", famous_city=city2)

session.add(place1)
session.commit()

place2 = FamousPlaces(name='Bannerghatta National Park',
                      description="Bannerghatta National Park, "
                      "near Bangalore, Karnataka, was founded in 1970"
                      " and declared as a national park in 1974. "
                      "In 2002 a portion of the park, became a "
                      "biological reserve, the Bannerghatta Biological Park.",
                      address="Bannerghatta Road, Bannerghatta, Bengaluru,"
                      " Karnataka 560083", famous_city=city2)

session.add(place2)
session.commit()

place3 = FamousPlaces(name='Bangalore Palace',
                      description="Bangalore Palace, a palace located "
                      "in Bengaluru, Karnataka, India, in an area owned"
                      " originally by Rev. J. Garrett, who was the "
                      "first Principal of the Central High School in Bangalore"
                      ", now known as Central College.", address="Palace "
                      "Road, Near Mount Carmel Institute Of Management, "
                      "Vasanth Nagar, Bengaluru, Karnataka 560052",
                      famous_city=city2)

session.add(place3)
session.commit()

city3 = FamousCities(name='Delhi')

session.add(city3)
session.commit()

place1 == FamousPlaces(name='The Red Fort',
                       description="The Delhi Gate is an entrance to "
                       "the Red Fort in Delhi and is on the Fort's "
                       "southern wall. The gate received its name "
                       "from the Fort's city. The primary gate is "
                       "the Lahori Gate, which is very similar in appearance.",
                       address="Netaji Subhash Marg, Lal Qila, Chandni Chowk,"
                       " New Delhi, Delhi 110006", famous_city=city3)

session.add(place1)
session.commit()

place2 = FamousPlaces(name='Qutub Minar',
                      description="Qutub Minar is a minaret that forms "
                      "part of the Qutb complex, a UNESCO World Heritage"
                      " Site in the Mehrauli area of Delhi, India. "
                      "Qutab Minar is a soaring, 73 m-high tower of victory,"
                      " built in 1193 by Qutab-ud-din Aibak immediately "
                      "after the defeat of Delhi's last Hindu kingdom.",
                      address='Mehrauli, New Delhi, Delhi 110030',
                      famous_city=city3)

session.add(place2)
session.commit()

place3 = FamousPlaces(name='India Gate',
                      description="At the centre of New Delhi stands"
                      " the 42 m high India Gate, an Arc-de-Triomphe "
                      "like archway in the middle of a crossroad. "
                      "Almost similar to its French counterpart, "
                      "it commemorates the 70,000 Indian soldiers who lost"
                      " their lives fighting for the British Army during "
                      "the World War I. The memorial bears the names of more"
                      " than 13,516 British and Indian soldiers killed in "
                      "the Northwestern Frontier in the Afghan war of 1919.",
                      address="Rajpath Marg, India Gate, New Delhi, "
                      "Delhi 110001", famous_city=city3)

session.add(place3)
session.commit()

city4 = FamousCities(name='Chandigarh')

session.add(city4)
session.commit()

place1 = FamousPlaces(name='Rock Garden',
                      description="The Rock Garden of Chandigarh is a "
                      "sculpture garden in Chandigarh, India, "
                      "also known as Nek Chand's Rock Garden after "
                      "its founder Nek Chand, a government official "
                      "who started the garden secretly in his spare time "
                      "in 1957", address="Rock Garden, Sector 1, "
                      "Chandigarh, 160001", famous_city=city4)

session.add(place1)
session.commit()

place2 = FamousPlaces(name='Sukhna Lake',
                      description="Sukhna Lake in Chandigarh, India,"
                      " is a reservoir at the foothills of the Himalayas."
                      " This 3 square km rainfed lake was created in 1958 "
                      "by damming the Sukhna Choe, a seasonal stream"
                      " coming down from the Shivalik Hills.",
                      address='Sukhna Lake, Sector 1, 160001',
                      famous_city=city4)

session.add(place2)
session.commit()

print "added famous places!"
