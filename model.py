from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Integer, String, DATETIME
from sqlalchemy.orm import sessionmaker, scoped_session, relationship, backref
# import seed

ENGINE = create_engine("sqlite:///ratings.db", echo=False)
session = scoped_session(sessionmaker(bind=ENGINE,
                                      autocommit = False,
                                      autoflush = False))

Base = declarative_base()
Base.query = session.query_property()

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
    movie_id = Column(Integer, ForeignKey('movies.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    rating = Column(Integer)

    user = relationship("User",
                         backref=backref("ratings", order_by=id))
    movie = relationship("Movie",
                         backref=backref("movies", order_by=id))


### End class declarations

### Functions

def create_user():
    pass

def add_rating():
    pass

def update_rating():
    pass

def authenticate(username, password):
    # query = """SELECT id, username, password FROM users WHERE username = ?"""
    # DB.execute(query, (username,))
    # row = DB.fetchone()

    if password == # int(row[2]):
        return row[0]
    else:
        return None




### End functions



def main():
    # """In case we need this for something"""
    pass

if __name__ == "__main__":
    main()
