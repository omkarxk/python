from flask import Flask, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "expense_secret"

# ---------- DATABASE ----------
def init_db():
    db = sqlite3.connect("expense.db")
    cur = db.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)")
    cur.execute("""CREATE TABLE IF NOT EXISTS expenses
                   (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT, amount INTEGER)""")
    cur.execute("INSERT OR IGNORE INTO users VALUES ('user', '1234')")
    db.commit()
    db.close()

init_db()

# ---------- LOGIN ----------
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        u = request.form["username"]
        p = request.form["password"]

        db = sqlite3.connect("expense.db")
        cur = db.cursor()
        cur.execute("SELECT * FROM users WHERE username=? AND password=?", (u, p))
        user = cur.fetchone()
        db.close()

        if user:
            session["user"] = u
            return redirect("/dashboard")
        return "<h3>Invalid Login</h3>"

    return """
    <html>
    <head>
        <title>Login</title>
        <style>
            body{font-family:Arial;text-align:center;background:#f4f4f4}
            input,button{padding:10px;margin:5px}
        </style>
    </head>
    <body>
        <h2>Expense Tracker Login</h2>
        <form method="post">
            <input name="username" placeholder="Username" required><br>
            <input type="password" name="password" placeholder="Password" required><br>
            <button>Login</button>
        </form>
    </body>
    </html>
    """

# ---------- DASHBOARD ----------
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/")

    db = sqlite3.connect("expense.db")
    cur = db.cursor()
    cur.execute("SELECT * FROM expenses")
    data = cur.fetchall()
    db.close()

    rows = ""
    total = 0
    for d in data:
        total += d[2]
        rows += f"""
        <tr>
            <td>{d[1]}</td>
            <td>₹{d[2]}</td>
            <td><a href="/delete/{d[0]}">❌</a></td>
        </tr>
        """

    return f"""
    <html>
    <head>
        <title>Dashboard</title>
        <style>
            body{{font-family:Arial;text-align:center}}
            table{{margin:auto;border-collapse:collapse}}
            td,th{{border:1px solid black;padding:8px}}
        </style>
    </head>
    <body>
        <h2>Welcome, {session['user']}</h2>
        <a href="/add">Add Expense</a> |
        <a href="/logout">Logout</a>

        <h3>Total Expense: ₹{total}</h3>

        <table>
            <tr><th>Title</th><th>Amount</th><th>Delete</th></tr>
            {rows}
        </table>
    </body>
    </html>
    """

# ---------- ADD EXPENSE ----------
@app.route("/add", methods=["GET", "POST"])
def add():
    if "user" not in session:
        return redirect("/")

    if request.method == "POST":
        title = request.form["title"]
        amount = request.form["amount"]

        db = sqlite3.connect("expense.db")
        cur = db.cursor()
        cur.execute("INSERT INTO expenses (title, amount) VALUES (?, ?)", (title, amount))
        db.commit()
        db.close()

        return redirect("/dashboard")

    return """
    <html>
    <head>
        <title>Add Expense</title>
        <style>
            body{font-family:Arial;text-align:center}
            input,button{padding:10px;margin:5px}
        </style>
    </head>
    <body>
        <h2>Add Expense</h2>
        <form method="post">
            <input name="title" placeholder="Expense Title" required><br>
            <input name="amount" type="number" placeholder="Amount" required><br>
            <button>Add</button>
        </form>
        <br><a href="/dashboard">Back</a>
    </body>
    </html>
    """

# ---------- DELETE ----------
@app.route("/delete/<int:id>")
def delete(id):
    if "user" not in session:
        return redirect("/")

    db = sqlite3.connect("expense.db")
    cur = db.cursor()
    cur.execute("DELETE FROM expenses WHERE id=?", (id,))
    db.commit()
    db.close()

    return redirect("/dashboard")

# ---------- LOGOUT ----------
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
