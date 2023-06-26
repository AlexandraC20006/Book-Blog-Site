
###############################################################
##                                                           ##
##   NOTE: School computers wipe every time you log off!     ##
##         In terminal, write "pip install flask-session"    ##
##         every time you log back on                        ##
##                                                           ##
###############################################################


from flask import Flask, render_template, request, session, redirect, url_for
from flask_session import Session
import sqlite3


app = Flask(__name__)


# Configure the app to use sessions
app.config["SESSION_TYPE"] = "filesystem"
Session(app)



# for signin i used the tutorial https://realpython.com/introduction-to-flask-part-2-creating-a-login-page/
@app.route("/sign_in", methods = ["GET", "POST"]) #sign in page
def sign_in():
    # user_id = session.get("user_id") # Retrieve a value from the session

    error = None
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username != "admin" or password != "admin": #check if input is correct
            error = "Incorrect username or password. Please try again." #error message if input is wrong
        else:
            session["username"] = username # Store a value in the session
            session["logged_in"] = True # Store a value in the session
            return redirect(url_for("home")) #if correct, takes you to home page
    return render_template("sign_in.html", error=error)


@app.route("/") #home page
def home():
    if session.get("logged_in") == True:
        return render_template("home_si.html") #takes you to signed in home page
    else:
        return render_template("home_so.html") #takes you to signed out home page


@app.route("/allbooks")
def all_books():
    conn = sqlite3.connect("bookshelf.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM Book")
    results = cur.fetchall()
    print(results)
    return render_template("all_books.html", results = results)


@app.route("/sign_out")
def sign_out():
    session["logged_in"] = False
    return render_template("sign_out.html")


if __name__ == "__main__":
    app.run(debug=True)