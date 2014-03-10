from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Integer, String, DATETIME
from sqlalchemy.orm import sessionmaker, scoped_session, relationship, backref
from operator import itemgetter
import correlation
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

    def similarity(self, other):
        u_ratings = {}
        paired_ratings = []
        for r in self.ratings:
            u_ratings[r.movie_id] = r

        for r in other.ratings:
            u_r = u_ratings.get(r.movie_id)
            if u_r:
                paired_ratings.append( (u_r.rating, r.rating) )

        if paired_ratings:
            return correlation.pearson(paired_ratings)
        else:
            return 0.0

    def predict_rating(self, movie):
        ratings = self.ratings
        other_ratings = movie.ratings
        similarities = [ (self.similarity(r.user), r)\
            for r in other_ratings ]
        similarities.sort(reverse=True)
        similarities = [sim for sim in similarities  if sim[0] > 0]
        if not similarities:
            return None
        numerator = sum([ r.rating * similarity for similarity, r in similarities ])
        denominator = sum([ similarity[0] for similarity in similarities ])
        return numerator/denominator

        # top_user = similarities[0]
        # return top_user[1].rating * top_user[0]



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
                         backref=backref("ratings", order_by=id))


### End class declarations

### Functions

def get_user_data(user_id):
    user_data = []
    user = session.query(User).get(user_id)
    ratings = user.ratings
    for rating in ratings:
        user_data.append((rating.movie.name, rating.movie.released_at.year, rating.rating, rating.movie.id))
    user_data = sorted(user_data, key=itemgetter(1))

    return user_data

def create_user(email, password, age, zipcode):
    u = User(email=email, password=password, age=age, zipcode=zipcode)
    session.add(u)
    session.commit()
    return u.id

def get_all_users():
    user_list = session.query(User).all()
    return user_list

def get_all_movies():
    movie_list = []
    all_movies = session.query(Movie).all()
    for movie in all_movies:
        movie_list.append((movie.id, movie.name, movie.released_at))
    movie_list = sorted(movie_list, key=itemgetter(2))
    return movie_list

def average_rating(movie_id):
    # get avg rating; takes a movie ID as an argument
    ratings = session.query(Rating).filter_by(movie_id=movie_id)
    ratings = [r.rating for r in ratings]
    mean = sum(ratings)/len(ratings)
    return mean

def get_movie_data(movie_id, user_id):
    # generate the average rating for the given movie
    this_movie_average = average_rating(movie_id)
    # generate the data for this particular movie (name, release dat, imdb url)
    movie_data = session.query(Movie).get(movie_id)
    name = movie_data.name
    released_at = movie_data.released_at.year
    imdb_url = movie_data.imdb_url
    # throw that info into a variable to be returned by the function
    this_movie_data = [movie_id, name, released_at, imdb_url]
    # get the ratings for the movie
    movie_ratings = session.query(Rating).filter_by(movie_id=movie_id)
    # append the ratings for this movie to a list
    this_movie_ratings= []
    for r in movie_ratings:
        rater = r.user_id
        rating = r.rating
        this_movie_ratings.append((rater, rating))
    # get the currently logged-in user's rating
    user_rating = get_user_rating(movie_id, user_id)
    
    return this_movie_average, this_movie_data, this_movie_ratings, user_rating

def get_user_rating(movie_id, user_id):
    user_rating = session.query(Rating).filter_by(movie_id=movie_id, user_id=user_id)
    user_rated = False
    for r in user_rating:
        user_rated = True
    if user_rated:
        user_rating = user_rating[0].rating
    else:
        user_rating = None

    return user_rating

def update_rating(movie_id, user_id, user_rating):
    old_rating = session.query(Rating).filter_by(movie_id=movie_id, user_id=user_id)
    if get_user_rating(movie_id, user_id):
        old_rating[0].rating = user_rating
        r = old_rating
    else:
        r = Rating(movie_id=movie_id, user_id=user_id, rating=user_rating)
        session.add(r)
    session.commit()
    return None

def authenticate(user_id, password):
    user = session.query(User).get(user_id)
    pw = user.password

    if password == pw:
        return user.id
    else:
        return None
    pass



### Correlation functions




### End functions
# TODO write comments


def main():
    # """In case we need this for something"""
    pass

if __name__ == "__main__":
    main()
