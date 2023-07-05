import requests
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
from io import BytesIO
import threading
import info
from Login import login
import subprocess
from Login import user

API_BASE = "https://openlibrary.org"
COVER_BASE = "https://covers.openlibrary.org/b/id"

root = Tk()
root.title("My GUI")
root.state('zoomed')

def load_images_async(books, box_x, box_y):
    for book in books:
        olid = book.get('cover_edition_key')
        if olid:
            title = book.get('title', 'N/A')
            authors = book.get('authors', [{'name': 'Unknown Author'}])
            cover_image = f"{COVER_BASE}/{book.get('cover_id')}-L.jpg"

            # Frame
            box_frame = Frame(frame1, width=160, height=280, bg="#FFFFFF")
            box_frame.place(x=box_x, y=box_y)

            book_cover_image(cover_image, box_frame, book)

            # Retrieve book details
            book_key = book.get('key')
            book_url = f"{API_BASE}/{book_key}.json"
            book_response = requests.get(book_url)
            book_data = book_response.json()

            # Update coordinates for the next box
            box_x += 200
            if box_x > root.winfo_screenwidth() - 140:
                if box_y > 7:
                    box_y += 68
                box_x = 138
                box_y += 250


# Frame 1
frame1 = Frame(root, bg="#2C2F30")
frame1.pack(fill=BOTH, expand=True)

# Line 1
line1 = Frame(frame1, width=root.winfo_screenwidth(), height=1, bg="#4F4F4F")
line1.place(x=0, y=63)

# E-Lib
elib = Label(frame1, text="E-Lib", bg="#2C2F30", fg="#FFFFFF", font=("Arial", 15, "bold"))
elib.place(x=35, y=20)

# Login
login_label = Label(frame1, text="Login", bg="#A71F01", fg="#FFFFFF", font=("Arial", 12, "bold"), cursor="hand2")
login_label.place(x=root.winfo_screenwidth() - 100, y=19)

try:
    response = requests.get(
        f"{API_BASE}/subjects/thriller.json?limit=6&sort=random")

    if response.status_code == 200:
        data = response.json()
        books = data.get('works', [])

        # total number of books
        print(f"Total books found: {len(books)}")

        # Call the load_images_async function in the background
        threading.Thread(target=load_images_async, args=(books, 138, 110)).start()

    else:
        print("Something went wrong!")

except requests.exceptions.RequestException as e:
    print(f"Request Exception: {e}")

def book_cover_image(cover_image, box_frame,book):
    try:
        # Rectangle 19
        rectangle19 = Frame(box_frame, width=120, height=150, bg="#FFFFFF")
        rectangle19.place(x=0, y=0)
        # Image section
        cover_image_response = requests.get(cover_image)
        cover_image_data = BytesIO(cover_image_response.content)
        image = Image.open(cover_image_data)
        # Resize image to fit within the frame size
        image = image.resize((155, 277))
        photo = ImageTk.PhotoImage(image)

        image_label = Label(rectangle19, image=photo, bg="#FFFFFF")
        image_label.image = photo  # Prevent image from being garbage collected
        image_label.pack(anchor=NW)
    except requests.exceptions.RequestException as e:
        print(f"Error loading image: {e}")
    image_label.bind('<Button-1>',lambda event, book=book: image_click(event, book))

def image_click(event,book):
    if not user.islogged:
        messagebox.showinfo("Login Required", "You need to login first.")
        if user.islogged:
            # Proceed with the desired action after successful login
            info.clicked_image(book)
            execute_trying()
        else:
            # Handle login failure if needed
            messagebox.showinfo(
                "Login Failed", "Login failed. Please try again.")
    else:
        info.clicked_image(book)

def login_function(event):
    if not user.islogged:

        login(event)
        if user.islogged:
            execute_trying()
    else:
        messagebox.showinfo("Logged In", "You are already logged in!")

login_label.bind('<Button-1>', login_function)

def execute_trying():
    try:
        subprocess.call(["python", "Login.py"])
    except Exception as e:
        print(f"Error executing Login.py: {e}")

root.mainloop()