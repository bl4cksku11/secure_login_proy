from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
import hashlib

# Configuración para vaciar la base de datos al iniciar la aplicación
VACIAR_BASE_DE_DATOS = False  # Cambia a True para vaciar la base de datos

app = Flask(__name__)
app.secret_key = 'tu_super_secreto'

def vaciar_base_de_datos():
    if VACIAR_BASE_DE_DATOS:
        conn = sqlite3.connect("userdata.db")
        cur = conn.cursor()
        # Aquí deberías verificar si la tabla existe antes de intentar borrarla
        cur.execute("DROP TABLE IF EXISTS userdata")
        # Aquí deberías volver a crear la tabla después de borrarla
        cur.execute("CREATE TABLE userdata (username TEXT UNIQUE, password TEXT)")
        conn.commit()
        conn.close()

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        conn = sqlite3.connect("userdata.db")
        cur = conn.cursor()
        cur.execute("SELECT * FROM userdata WHERE username = ? AND password = ?", (username, hashed_password))
        user = cur.fetchone()
        conn.close()

        if user:
            session['username'] = username
            return redirect(url_for('success'))
        else:
            flash('Login Failed!')

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash("Passwords do not match!")
            return redirect(url_for('register'))

        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        conn = sqlite3.connect("userdata.db")
        cur = conn.cursor()

        try:
            cur.execute("INSERT INTO userdata (username, password) VALUES (?, ?)", (username, hashed_password))
            conn.commit()
        except sqlite3.IntegrityError:
            flash("Username already exists!")
        else:
            flash("Registered successfully!")
            return redirect(url_for('login'))
        finally:
            conn.close()

    return render_template('register.html')

@app.route('/success')
def success():
    if 'username' in session:
        return render_template('success.html', username=session['username'])
    else:
        flash("You must be logged in to view this page.")
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash("You have been logged out.")
    return redirect(url_for('login'))

if __name__ == '__main__':
    vaciar_base_de_datos()
    app.run(debug=True, host='0.0.0.0', port=9999)