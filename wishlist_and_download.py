import os
from tkinter import *
from tkinter import filedialog
import webbrowser
import mysql.connector
from tkinter import messagebox
import pyttsx3
from urllib.parse import quote_plus
from connection import connection
from Login import user

def speak_message():
    engine = pyttsx3.init()
    engine.setProperty('voices', 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\SPEECH_OneCore\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0')
    engine.say("Pay for your DAMN book!")
    engine.runAndWait()
def download(key, title):
    # Encode the key and title for URL usage
    encoded_title = quote_plus(title)

    # Open the specified link in a web browser.
    webbrowser.open(f"https://openlibrary.org/search?q={key}+{encoded_title}")

    # Call the speak_message function after opening the web browser
    speak_message()

def wishlist(book_name,author_name):
    user_name = user.get_user_info[name]
    
    # Create the wishlist table for the user
    create_wishlist_table(user_name)

    # Connect to the database
    conn, cur = connection()

    # Insert the book and author into the wishlist table
    table_name = f"{user_name}_wishlist"
    insert_query = f"INSERT INTO {table_name} (book_name, author_name) VALUES (%s, %s)"
    values = (book_name, author_name)
    cur.execute(insert_query, values)
    conn.commit()
    cur.close()

    print("Book added to wishlist successfully!")

def create_wishlist_table(username):
    # Connecting to the database
    conn, cur = connection()

    # Create a table for the user's wishlist
    table_name = f"{username}_wishlist"
    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        book_name VARCHAR(255),
        author_name VARCHAR(255)
    )
    """
    cur.execute(create_table_query)
    conn.commit()
    cur.close()

if __name__ =='__main__':
    root = Tk()
    root.title('idk')
    root.geometry('300x400')
    
    '''download_button = Button(root, text="Download")
    download_button.pack()
    
    title = "A_Gentleman_in_Moscow"
    key = "OL26386597M"
    
    download_button.bind('<Button-1>', download(key,title))'''
    
    # Get the user's input for book name and author
    book_name = input("Enter book name: ")
    author_name = input("Enter author name: ")

    # Get the logged-in user's name from the login module
    user_name = "John"  # Replace with the actual name retrieved from the login module
    
    wishlist_button = Button(root,text="Wishlist")
    wishlist_button.pack()
    
    wishlist_button.bind('<Button-1>',wishlist(book_name,author_name))
    
    root.mainloop()