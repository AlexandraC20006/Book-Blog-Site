
#############################################################
#                                                           #
#   NOTE: School computers wipe every time you log off!     #
#         In terminal, write "pip install flask-session"    #
#         every time you log back on                        #
#                                                           #
#############################################################


from flask import Flask, render_template, request, session, redirect, url_for
from flask_session import Session
import sqlite3


app = Flask(__name__)


# Configure the app to use sessions
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# for signin i used the tutorial https://realpython.com/introduction-to-flask-part-2-creating-a-login-page/
@app.route("/sign_in", methods=["GET", "POST"])  # sign in page
def sign_in():
    # user_id = session.get("user_id") # Retrieve a value from the session

    error = None
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        # check if input is correct
        if username != "admin" or password != "admin":
            # error message if input is wrong
            error = "Incorrect username or password. Please try again."
        else:
            # Store values in the session
            session["username"] = username
            session["logged_in"] = True
            # if correct, takes you to home page
            return redirect(url_for("home"))
    return render_template("sign_in.html", error=error)


@app.route("/")  # home page
def home():
    if session.get("logged_in") is True:
        # takes you to signed in home page
        return render_template("home_si.html")
    else:
        # takes you to signed out home page
        return render_template("home_so.html")


@app.route("/allbooks")
def all_books():
    conn = sqlite3.connect("bookshelf.db")
    cur = conn.cursor()
    cur.execute("SELECT Book.id, Book.title, Book.image, Author.name FROM Book JOIN BookAuthor ON Book.id = BookAuthor.bid JOIN Author ON Author.id = BookAuthor.aid")
    results = cur.fetchall()
    return render_template("all_books.html", results=results)


@app.route("/sign_out")
def sign_out():
    session["logged_in"] = False
    return render_template("sign_out.html")


@app.route("/authors")
def authors():
    conn = sqlite3.connect("bookshelf.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM Author")
    results = cur.fetchall()
    return render_template("author.html", results=results)


@app.route("/genres")
def genres():
    conn = sqlite3.connect("bookshelf.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM Genre")
    results = cur.fetchall()
    return render_template("genre.html", results=results)

# "SELECT Author.id, Author.name, FROM Author JOIN BookAuthor ON BookAuthor.aid = Author.id JOIN Book ON Book.id = BookAuthor.bid"


if __name__ == "__main__":
    app.run(debug=True)
