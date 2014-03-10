from flask import Flask, render_template, redirect, request, url_for, session, flash
import model

app = Flask(__name__)
app.secret_key="seeeeeeeeeeeecret"

@app.route("/")
def index():
    if session.get("user_id"):
        # user_id = session["user_id"]
        return redirect(url_for("all_movies"))
    else:
        return render_template("login.html")

@app.route("/", methods=["POST"])
def process_login():
    user_id = request.form.get("user_id")
    password = request.form.get("password")
    user_id = model.authenticate(user_id, password)
    if user_id:
        flash("User authenticated")
        session["user_id"] = user_id
    else:
        flash("WRONG.")

    return redirect(url_for("index"))    

@app.route("/register")
def register():
    if session.get("user_id"):
        return redirect(url_for("user_profile", user_id=session.get("user_id")))
    else:
        return render_template("create_user.html")


@app.route("/register", methods=["POST"])
def create_account():
    email = request.form.get("email")
    password = request.form.get("password")
    age = request.form.get("age")
    zipcode = request.form.get("zipcode")
    user_id = model.create_user(email=email, password=password, age=age, zipcode=zipcode)
    flash("Your user id is: %s" % user_id)
    return redirect(url_for("index")) 

@app.route("/my_profile")
def view_profile():
    user_id=session.get("user_id")
    if user_id:
        return redirect(url_for("user_profile", user_id=user_id))
    else:
        return redirect(url_for("register"))

@app.route("/all_users")
def all_users():
    user_list = model.get_all_users()
    return render_template("user_list.html", user_list=user_list)

@app.route("/all_movies")
def all_movies():
    movie_list = model.get_all_movies()
    return render_template("movie_list.html", movie_list=movie_list)

@app.route("/user/<user_id>")
def user_profile(user_id):
    user_data = model.get_user_data(user_id)
    return render_template("user_profile.html", user_data=user_data, user_id=user_id)

@app.route("/movie/<movie_id>")
def view_movie(movie_id):
    user_id = session.get("user_id")
    avg, data, ratings, user_rating = model.get_movie_data(movie_id, user_id)

    # Prediction code: onles used if the user hasn't already rated it
    user = model.session.query(model.User).get(session['user_id'])
    movie = model.session.query(model.Movie).get(movie_id)
    prediction = None
    u_rating = None
    if user_rating:
        u_rating = model.session.query(model.Rating).filter_by(user_id=user_id, movie_id=movie_id).first()
    if not u_rating:
        prediction = user.predict_rating(movie)
        effective_rating = prediction
    else:
        effective_rating = u_rating.rating

    the_eye = model.session.query(model.User).filter_by(email="varchar@hackbright.com").one()
    eye_rating = model.session.query(model.Rating).filter_by(user_id=the_eye.id, movie_id=movie.id).first()

    if not eye_rating:
        eye_rating = the_eye.predict_rating(movie)
    else:
        eye_rating = eye_rating.rating

    if not eye_rating:
        beratement = "What do you think?"
    else:

        difference = abs(eye_rating - effective_rating)

        messages = [ "I suppose you don't have such bad taste after all. VARCHAR APPROVES!",
                     "I regret every decision that I've ever made that has brought me to listen to your opinion.",
                     "Words fail me, as your taste in movies has clearly failed you.",
                     "That movie is great. For a clown to watch. Idiot."]

        beratement = messages[int(difference)]

    return render_template("movie.html", data=data, avg=avg, ratings=ratings, this_user=int(user_id), user_rating=user_rating, prediction=prediction, beratement=beratement)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/movie/<movie_id>', methods=["POST"])
def edited_rating(movie_id):
    user_id = session.get("user_id")
    user_rating = request.form.get("rating")
    model.update_rating(movie_id, user_id, user_rating)
    return redirect(url_for("view_movie", movie_id=movie_id))

if __name__ == "__main__":
    app.run(debug = True)