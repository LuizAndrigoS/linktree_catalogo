from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'chave_secreta_simples'

def get_db_connection():
    conn = sqlite3.connect('catalogos.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def index():
    conn = get_db_connection()
    catalogos = conn.execute('SELECT * FROM catalogos').fetchall()
    conn.close()
    return render_template("index.html", catalogos=catalogos)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form["username"] == "admin" and request.form["password"] == "senha123":
            session["admin"] = True
            return redirect(url_for("admin"))
        else:
            return "Login inválido!"
    return render_template("login.html")

@app.route("/admin", methods=["GET", "POST"])
def admin():
    if not session.get("admin"):
        return redirect(url_for("login"))

    conn = get_db_connection()
    if request.method == "POST":
        nome = request.form["nome"]
        link = request.form["link"]
        conn.execute("INSERT INTO catalogos (nome, link) VALUES (?, ?)", (nome, link))
        conn.commit()

    catalogos = conn.execute("SELECT * FROM catalogos").fetchall()
    conn.close()
    return render_template("admin.html", catalogos=catalogos)

@app.route("/delete/<int:id>")
def delete(id):
    if not session.get("admin"):
        return redirect(url_for("login"))
    conn = get_db_connection()
    conn.execute("DELETE FROM catalogos WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for("admin"))

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)