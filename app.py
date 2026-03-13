import sqlite3
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect("todo.db")
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/")
def home():
    conn = get_db_connection()
    tasks = conn.execute("SELECT * FROM tasks").fetchall()
    conn.close()
    return render_template("index.html", tasks=tasks)


@app.route("/add", methods=["POST"])
def add():
    task = request.form["task"]
    conn = get_db_connection()
    conn.execute("INSERT INTO tasks (task) VALUES (?)", (task,))
    conn.commit()
    conn.close()
    return redirect("/")


@app.route("/delete/<int:id>")
def delete(id):
    conn = get_db_connection()
    conn.execute("DELETE FROM tasks WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect("/")


@app.route("/complete/<int:id>")
def complete(id):
    conn = get_db_connection()
    conn.execute("UPDATE tasks SET completed=1 WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect("/")

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    conn = get_db_connection()

    if request.method == "POST":
        new_task = request.form["task"]
        conn.execute("UPDATE tasks SET task=? WHERE id=?", (new_task, id))
        conn.commit()
        conn.close()
        return redirect("/")

    task = conn.execute("SELECT * FROM tasks WHERE id=?", (id,)).fetchone()
    conn.close()
    return render_template("edit.html", task=task)

if __name__ == "__main__":
    app.run(debug=True, port=5001)