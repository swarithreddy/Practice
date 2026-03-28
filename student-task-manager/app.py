from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

# Create table if not exists
def init_db():
    conn = get_db_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

init_db()

@app.route("/", methods=["GET", "POST"])
def home():
    conn = get_db_connection()

    if request.method == "POST":
        task = request.form.get("task")
        conn.execute("INSERT INTO tasks (content) VALUES (?)", (task,))
        conn.commit()
        return redirect("/")

    tasks = conn.execute("SELECT * FROM tasks").fetchall()
    conn.close()

    return render_template("index.html", tasks=tasks)

if __name__ == "__main__":
    app.run(debug=True)
