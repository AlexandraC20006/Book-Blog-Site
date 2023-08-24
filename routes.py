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
import math


app = Flask(__name__)


# Configure the app to use sessions
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# for signin i used the tutorial
# https://realpython.com/introduction-to-flask-part-2-creating-a-login-page/
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


@app.route("/allbooks")  # All books on one page
def all_books():
    conn = sqlite3.connect("bookshelf.db")
    cur = conn.cursor()
    # Finds the book id, title, image and author of every book
    cur.execute("SELECT Book.id, \
        Book.title, \
        Book.image, \
        Author.name \
        FROM Book \
        JOIN BookAuthor ON Book.id = BookAuthor.bid \
        JOIN Author ON Author.id = BookAuthor.aid;")
    results = cur.fetchall()
    row_amount = len(results)/3
    rows = math.ceil(row_amount)  # rows of images to display
    return render_template("all_books.html", results=results, rows=rows)


@app.route("/sign_out")  # changes your session from logged in to logged out
def sign_out():
    session["logged_in"] = False
    return render_template("sign_out.html")


@app.route("/authors")  # List of authors, they link to a page with their books
def all_authors():
    conn = sqlite3.connect("bookshelf.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM Author")
    results = cur.fetchall()
    return render_template("all_authors.html", results=results)


@app.route("/author/<int:id>")  # automatic page with author's books
def author(id):
    conn = sqlite3.connect("bookshelf.db")
    cur = conn.cursor()
    cur.execute("SELECT BookAuthor.aid, \
            Book.id, \
            Book.title, \
            Book.image, \
            Author.name \
        FROM Book \
            JOIN \
            BookAuthor ON BookAuthor.bid = Book.id \
            JOIN \
            Author ON Author.id = BookAuthor.aid \
        WHERE BookAuthor.aid = ?;", (id,))
    results = cur.fetchall()
    return render_template("author_books.html", results=results)


@app.route("/genres")  # List of genres, they link to a page with their books
def all_genres():
    conn = sqlite3.connect("bookshelf.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM Genre")
    results = cur.fetchall()
    return render_template("all_genres.html", results=results)


@app.route("/genre/<int:id>")  # automatic page with books in a genre
def genre(id):
    conn = sqlite3.connect("bookshelf.db")
    cur = conn.cursor()
    cur.execute("SELECT BookGenre.gid, \
            Book.id, \
            Book.title, \
            Book.image, \
            Author.name \
        FROM Book \
            JOIN \
            BookGenre ON BookGenre.bid = Book.id \
            JOIN \
            BookAuthor ON BookAuthor.bid = Book.id \
            JOIN \
            Author ON Author.id = BookAuthor.aid \
        WHERE BookGenre.gid = ?;", (id,))
    results = cur.fetchall()
    return render_template("genre_books.html", results=results)


@app.route("/book_info/<int:id>")  # page displaying all info on one book
def book_info(id):
    conn = sqlite3.connect("bookshelf.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM Book WHERE id = ?;", (id,))
    book = cur.fetchone()
    cur.execute("SELECT Genre.name \
        FROM Genre \
            JOIN \
            BookGenre ON BookGenre.gid = Genre.id \
        WHERE BookGenre.bid = ?;", (id,))
    genres = cur.fetchall()
    cur.execute("SELECT Author.name \
        FROM Author \
            JOIN \
            BookAuthor ON BookAuthor.aid = Author.id \
        WHERE BookAuthor.bid = ?;", (id,))
    authors = cur.fetchall()
    return render_template("book_info.html", book=book, genres=genres, authors=authors)


if __name__ == "__main__":
    app.run(debug=True)
