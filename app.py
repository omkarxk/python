from flask import Flask, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "internship_secret"

# ---------- DATABASE ----------
def init_db():
    db = sqlite3.connect("data.db")
    cur = db.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS applications (company TEXT, role TEXT)")
    cur.execute("INSERT OR IGNORE INTO users VALUES ('student', '1234')")
    db.commit()
    db.close()

init_db()

# ---------- LOGIN ----------
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        u = request.form["username"]
        p = request.form["password"]

        db = sqlite3.connect("data.db")
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
            body{font-family:Arial;background:#f4f4f4;text-align:center}
            input,button{padding:10px;margin:5px}
        </style>
    </head>
    <body>
        <h2>Student Login</h2>
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

    db = sqlite3.connect("data.db")
    cur = db.cursor()
    cur.execute("SELECT * FROM applications")
    data = cur.fetchall()
    db.close()

    rows = ""
    for d in data:
        rows += f"<tr><td>{d[0]}</td><td>{d[1]}</td></tr>"

    return f"""
    <html>
    <head>
        <title>Dashboard</title>
        <style>
            body{{font-family:Arial;text-align:center}}
            table{{margin:auto;border-collapse:collapse}}
            td,th{{border:1px solid #000;padding:8px}}
        </style>
    </head>
    <body>
        <h2>Welcome, {session['user']}</h2>
        <a href="/apply">Apply Internship</a> |
        <a href="/logout">Logout</a>

        <h3>Applications</h3>
        <table>
            <tr><th>Company</th><th>Role</th></tr>
            {rows}
        </table>
    </body>
    </html>
    """

# ---------- APPLY ----------
@app.route("/apply", methods=["GET", "POST"])
def apply():
    if "user" not in session:
        return redirect("/")

    if request.method == "POST":
        company = request.form["company"]
        role = request.form["role"]

        db = sqlite3.connect("data.db")
        cur = db.cursor()
        cur.execute("INSERT INTO applications VALUES (?, ?)", (company, role))
        db.commit()
        db.close()

        return redirect("/dashboard")

    return """
    <html>
    <head>
        <title>Apply</title>
        <style>
            body{font-family:Arial;text-align:center}
            input,button{padding:10px;margin:5px}
        </style>
    </head>
    <body>
        <h2>Apply for Internship</h2>
        <form method="post">
            <input name="company" placeholder="Company Name" required><br>
            <input name="role" placeholder="Role" required><br>
            <button>Submit</button>
        </form>
        <br><a href="/dashboard">Back</a>
    </body>
    </html>
    """

# ---------- LOGOUT ----------
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
