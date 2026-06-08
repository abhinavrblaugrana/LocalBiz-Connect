import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

DB_NAME = "localbiz.db"


def get_connection():
    conn=sqlite3.connect(DB_NAME)
    conn.row_factory=sqlite3.Row
    return conn


def create_tables():
    conn=get_connection()
    cur=conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        password_hash TEXT NOT NULL
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS enquiries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                phone TEXT NOT NULL,
                service TEXT NOT NULL,
                message TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'Open'
    )
    """)

    conn.commit()
    conn.close()

def create_user(name, email, password):
    conn = get_connection()
    cur = conn.cursor()

    password_hash = generate_password_hash(password)

    cur.execute("""
    INSERT INTO users (name, email, password_hash)
    VALUES (?, ?, ?)
    """, (name, email, password_hash))

    conn.commit()
    conn.close()


def get_user_by_email(email):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM users WHERE email = ?", (email,))
    user = cur.fetchone()

    conn.close()
    return user


def check_user_password(user, password):
    return check_password_hash(user["password_hash"], password)


def insert_sample_data():
    conn=get_connection()
    cur=conn.cursor()

    cur.execute("SELECT COUNT(*) AS count FROM enquiries")
    count=cur.fetchone()["count"]

    if count==0:
        sample_data=[
            ("Akhil Raj", "akhil@example.com", "9876543210", "Website Design", "Need a website for my bakery", "Open"),
            ("Meera Thomas", "meera@example.com", "9876543211", "Digital Marketing", "Need Instagram promotion", "Open"),
            ("Nikhil Joseph", "nikhil@example.com", "9876543212", "IT Support", "Need computer support", "Completed"),
            ("Anu Mary", "anu@example.com", "9876543213", "App Development", "Need app idea discussion", "Completed")
        ]

        cur.executemany("""
        INSERT INTO enquiries (name,email,phone,service,message,status)
        VALUES (?,?,?,?,?,?)
        """, sample_data
        )

        conn.commit()
        conn.close()


def get_all_enquiries():
    conn=get_connection()
    cur=conn.cursor()

    cur.execute("SELECT * FROM  enquiries ORDER BY id DESC")
    rows=cur.fetchall()

    conn.close()
    return rows


def add_enquiry(name,email,phone,service,message):
    conn=get_connection()
    cur=conn.cursor()


    cur.execute("""
        INSERT INTO enquiries (name,email,phone,service,message,status)
        VALUES (?,?,?,?,?,'Open')
        """, (name,email,phone,service,message))
    
    conn.commit()
    conn.close()


def delete_enquiry(enquiry_id):
    conn=get_connection()
    cur=conn.cursor()


    cur.execute("DELETE FROM enquiries WHERE id=?",(enquiry_id,))

    conn.commit()
    conn.close()


def get_dashboard_counts():
    conn=get_connection()
    cur=conn.cursor()

    cur.execute("SELECT COUNT(*) AS count FROM enquiries")
    total=cur.fetchone()["count"]

    cur.execute("SELECT COUNT(*) AS count FROM enquiries WHERE status='Open'")
    open_count=cur.fetchone()["count"]

    cur.execute("SELECT COUNT(*) AS count FROM enquiries WHERE status='Completed'")
    completed=cur.fetchone()["count"]

    conn.close()

    return{
        "total_enquiries": total,
        "open_requests": open_count,
        "completed_works": completed
    }

