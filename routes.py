from flask import Flask, render_template
import sqlite3


app = Flask(__name__)


@app.route('/') #sign in page
def sign_in():
    return render_template("sign_in.html")


@app.route('/home') #home page
def home():
    return render_template("home.html")


@app.route('/allbooks')
def all_books():
    return render_template("all_books.html")


if __name__ == "__main__":
    app.run(debug=True)