import sqlite3
import hashlib

conn = sqlite3.connect("userdata.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS userdata (
            id INTEGER BINARY KEY,
            username VARCHAR(255) NOT NULL,
            password VARCHAR(255) NOT NULL
)
""")

username1, password1 = "SamyFuria23", hashlib.sha256("Samyp@ssword123".encode()).hexdigest()
username2, password2 = "Sethkaiser13", hashlib.sha256("Kaiser_King13".encode()).hexdigest()
username3, password3 = "MayleenCampines", hashlib.sha256("Leeny4life@23".encode()).hexdigest()
username4, password4 = "Nitoxxdtm", hashlib.sha256("nitolachupa".encode()).hexdigest()

cur.execute("INSERT INTO userdata (username, password) VALUES (?, ?)", (username1, password1))
cur.execute("INSERT INTO userdata (username, password) VALUES (?, ?)", (username2, password2))
cur.execute("INSERT INTO userdata (username, password) VALUES (?, ?)", (username3, password3))
cur.execute("INSERT INTO userdata (username, password) VALUES (?, ?)", (username4, password4))

# res= cur.execute("SELECT username FROM userdata")
# print(res.fetchall())

conn.commit()


