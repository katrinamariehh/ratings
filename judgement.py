from flask import Flask, render_template, redirect, request
import model

app = Flask(__name__)

@app.route("/")
def index():
    pass

@app.route("/register")
def register():
    pass

@app.route("/all_users")
def all_users():
    user_list = model.session.query(model.User).all()
    return render_template("user_list.html", user_list=user_list)

@app.route("/user/<username>")
def user_profile(username):
    pass

@app.route("/<movie>")
def view_movie():
    pass



if __name__ == "__main__":
    app.run(debug = True)