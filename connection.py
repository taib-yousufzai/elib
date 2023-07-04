import mysql.connector
from tkinter import messagebox

def connection():
    try:
        conn = mysql.connector.connect(host='localhost', user='root', passwd='', database='library')
        cur = conn.cursor()
        return conn, cur
    except Exception as e:
        messagebox.showerror('Error', f"Database connection failed: {e}")