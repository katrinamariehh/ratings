from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Integer, String, DATETIME
from sqlalchemy.orm import sessionmaker, scoped_session, relationship, backref
from operator import itemgetter
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

def get_user_data(user_id):
    user_data = []
    user = session.query(User).get(user_id)
    ratings = user.ratings
    for rating in ratings:
        user_data.append((rating.movie.name, rating.movie.released_at.year, rating.rating))
    user_data = sorted(user_data, key=itemgetter(1))

    return user_data

def create_user(email, password, age, zipcode):
    u = User(email=email, password=password, age=age, zipcode=zipcode)
    session.add(u)
    session.commit()
    return u.id

def get_movie_data(movie):
    pass

def add_rating():
    pass

def update_rating():
    pass

def authenticate(user_id, password):
    user = session.query(User).get(user_id)
    pw = user.password

    if password == pw:
        return user_id
    else:
        return None
    pass




### End functions



def main():
    # """In case we need this for something"""
    pass

if __name__ == "__main__":
    main()
