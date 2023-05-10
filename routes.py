from flask import Flask, render_template, request, session, redirect, url_for
import sqlite3


app = Flask(__name__)

# for signin i used the tutorial https://realpython.com/introduction-to-flask-part-2-creating-a-login-page/
@app.route("/", methods = ["GET", "POST"]) #sign in page
def sign_in():
    error = None
    if request.method == "POST":
        if request.form["username"] != "admin" or request.form["password"] != "admin": #check if input is correct
            error = "Incorrect username or password. Please try again." #error message if input is wrong
        else:
            return redirect(url_for("home")) #if correct, takes you to home page
    return render_template("sign_in.html", error=error)


@app.route("/home") #home page
def home():
    return render_template("home.html")


@app.route("/allbooks")
def all_books():
    conn = sqlite3.connect("bookshelf.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM Book")
    results = cur.fetchall()
    print(results)
    return render_template("all_books.html", results = results)


if __name__ == "__main__":
    app.run(debug=True)