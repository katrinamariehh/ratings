from flask import Flask, render_template, redirect, request, url_for, session, flash
import model

app = Flask(__name__)
app.secret_key="seeeeeeeeeeeecret"

@app.route("/")
def index():
    if session.get("user_id"):
        user_id = session["user_id"]
        return redirect(url_for("user_profile", user_id=user_id))
    else:
        return render_template("login.html")

@app.route("/", methods=["POST"])
def process_login():
    user_id = request.form.get("user_id")
    password = request.form.get("password")
    if model.authenticate(user_id, password):
        return redirect(url_for("user_profile", user_id=user_id))
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

@app.route("/all_users")
def all_users():
    user_list = model.session.query(model.User).all()
    return render_template("user_list.html", user_list=user_list)

@app.route("/user/<user_id>")
def user_profile(user_id):
    user_data = model.get_user_data(user_id)
    return render_template("user_profile.html", user_data=user_data, user_id=user_id)

@app.route("/<movie>")
def view_movie():
    pass



if __name__ == "__main__":
    app.run(debug = True)