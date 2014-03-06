from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DATETIME
from sqlalchemy.orm import sessionmaker
import seed

ENGINE = None
Session = None

Base = declarative_base()

### Class declarations go here
class User(Base):
    # creating a user object to be added to the database
    __tablename__ = "users"

    id = Column(Integer, primary_key = True)
    email = Column(String(64), nullable = True)
    password = Column(String(64), nullable = True)
    age = Column(Integer, nullable = True)
    zipcode = Column(String(15), nullable = True)

class Movie(Base):
    # creating a movie object to be added to the databse
    __tablename__ = "movies"

    id = Column(Integer, primary_key = True)
    name = Column(String(64), nullable = True)
    released_at = Column(DATETIME, nullable = True) #check datetime format
    imdb_url = Column(String, nullable = True) # may make us give str len?

class Rating(Base):
    # creating a Rating object to be added to the database
    __tablename__ = "ratings"

    id = Column(Integer, primary_key = True)
    movie_id = Column(Integer) # maybe make this nullable later?
    user_id = Column(Integer) # nullable???
    rating = Column(Integer)

### End class declarations

def connect():
    global ENGINE
    global Session

    ENGINE = create_engine("sqlite:///ratings.db", echo=True)
    Session = sessionmaker(bind=ENGINE)

    return Session()

def main():
    """In case we need this for something"""
    pass

if __name__ == "__main__":
    main()
