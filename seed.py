import model
import csv
import datetime

def load_users(session):
    with open('seed_data/u.user', 'rb') as f:
        reader = csv.reader(f, delimiter="|")
        for row in reader:
        # setting row info from file as an object to go into the database
            u_id, u_age, u_gender, u_pw, u_zip = row
            u = model.User(password=u_pw, age=u_age, zipcode=u_zip)
            u.id = u_id
            session.add(u)
    session.commit()


def load_movies(session):
    # use u.item
    with open('seed_data/u.item', 'rb') as f:
        # read in file using |s as delimiters -- don't split on commas
        reader = csv.reader(f, delimiter="|")
        for row_data in reader:
            id = row_data[0]
            name = row_data[1].decode("latin-1")
            name = name[:-6].strip()
            if len(row_data[2]) > 0:
                released_at = datetime.datetime.strptime(row_data[2], "%d-%b-%Y")
            imdb_url = row_data[4]
            if released_at:
                m = model.Movie(name=name, released_at=released_at, imdb_url=imdb_url)
            m.id=id
            session.add(m)
    session.commit()



def load_ratings(session):
    # use u.data
    with open('seed_data/u.data', 'rb') as f:
        reader = csv.reader(f, delimiter="\t")
        for row_data in reader:
            user_id, movie_id, rating, timestamp = row_data
            r = model.Rating(movie_id=movie_id, rating=rating, user_id=user_id)
            session.add(r)
    session.commit()



def main(session):
    load_users(session)
    load_movies(session)
    load_ratings(session)


if __name__ == "__main__":
    s= model.connect()
    main(s)
