import model
import csv
import datetime

def load_users(session):
    with open('seed_data/u.user', 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            row_data = row[0].split('|')
            u_id = row_data[0]
            u_age = row_data[1]
            u_pw = row_data[3]
            u_zip = row_data[4]
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
            u_id = row_data[0]
            u_name = row_data[1]
            u_release = datetime.datetime.strptime(row_data[2], "%d-%b-%Y")
            u_imdb = row_data[4]
            u = model.Movie(name=u_name, released_at=u_release, imdb_url=u_imdb)
            u.id=u_id
            session.add(u)
            session.commit()



def load_ratings(session):
    # use u.data
    pass

def main(session):
    # load_users(session)
    load_movies(session)


if __name__ == "__main__":
    s= model.connect()
    main(s)
