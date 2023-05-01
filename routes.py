from flask import Flask, render_template
import sqlite3


app = Flask(__name__)


@app.route('/') #sign in page
def sign_in():
    return render_template("sign_in.html")

if __name__ == "__main__":
    app.run(debug=True)