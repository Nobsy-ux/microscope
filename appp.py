from flask import Flask, request, render_template
import sqlite3

app = Flask(__name__)

def init_db():
    with sqlite3.connect("specimens.db") as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS specimens (
            username TEXT,
            microscope_size REAL,
            magnification REAL,
            actual_size REAL
        )''')

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        username = request.form["username"]
        microscope_size = float(request.form["microscope_size"])
        magnification = float(request.form["magnification"])
        actual_size = (microscope_size / magnification) * 1000

        with sqlite3.connect("specimens.db") as conn:
            conn.execute("INSERT INTO specimens VALUES (?, ?, ?, ?)",
                         (username, microscope_size, magnification, actual_size))
        return render_template("indexes.html", result=actual_size)
    return render_template("indexes.html")

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
