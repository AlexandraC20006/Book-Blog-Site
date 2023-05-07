from flask import Flask, render_template, request, session, redirect, url_for
import sqlite3


app = Flask(__name__)


@app.route('/', methods = ['GET', 'POST']) #sign in page
def sign_in():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Incorrect username or password. Please try again.'
        else:
            return redirect(url_for('home'))
    return render_template("sign_in.html", error=error)


@app.route('/home') #home page
def home():
    return render_template("home.html")


@app.route('/allbooks')
def all_books():
    conn = sqlite3.connect("bookshelf.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM Book")
    results = cur.fetchall()
    print(results)
    return render_template("all_books.html", results = results)


if __name__ == "__main__":
    app.run(debug=True)