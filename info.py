import requests
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
from io import BytesIO
from urllib.parse import quote_plus
import json
from Login import login
#why

API_BASE = "https://openlibrary.org"

def clicked_image(book_details):
    def update_display(book):
        # check if user is logged in
        '''if not user_data[0]:
            messagebox.showerror('ERROR','User is not logged in')#print("User is not logged in")
        return'''

        #displayt book information
        print(book)
        root = Tk()
        root.title("My GUI")
        root.state('zoomed')

        frame1 = Frame(root, bg='#2C2F30')
        frame1.pack(fill=BOTH, expand=True)

        elib = Label(frame1, text='E-Lib', bg="#2C2F30", fg="#FFFFFF", font=("Arial", 15, "bold"))
        elib.place(x=35, y=20)

        logout_label = Label(frame1, text="Logout", bg="#A71F01", fg="#FFFFFF", font=("Arial", 15, "bold"))
        logout_label.place(x=root.winfo_screenwidth() - 100, y=19)

        line1 = Frame(frame1, width=root.winfo_screenwidth(), height=3, bg='#4F4F4F')
        line1.place(x=0, y=63)

        box_frame = Frame(frame1, width=200, height=300, bg="#FFFFFF")
        box_frame.place(x=100, y=120)

        rectangle_19 = Frame(box_frame, width=120, height=150, bg="#FFFFFF")
        rectangle_19.place(x=0, y=0)

        rectangle_31 = Frame(frame1, width=860, height=325, bg="#282828")
        rectangle_31.place(x=400, y=120)

        Book_Title = Label(rectangle_31, text="Book Title:", font=('Arial', 20), fg='#FFFFFF', bg="#282828")
        Book_Title.place(x=20, y=50)

        author = Label(rectangle_31, text="Author:", font=('Arial', 20), fg='#FFFFFF', bg="#282828")
        author.place(x=20, y=100)

        ISBN = Label(rectangle_31, text="ISBN:", font=('Arial', 20), fg='#FFFFFF', bg="#282828")
        ISBN.place(x=20, y=160)

        Publication = Label(rectangle_31, text="Publication:", font=('Arial', 20), fg='#FFFFFF', bg="#282828")
        Publication.place(x=20, y=210)

        Download = Button(rectangle_31, text="Download", width=10, height=2, font=("Arial", 13), bg='#A71F01', fg="#FFFFFF",relief='raised')
        Download.place(x=20, y=260)

        Wishlist = Button(rectangle_31, text="Add to wishlist", width=15, height=2, font=("Arial", 13), bg="#A71F01", fg="#FFFFFF",relief='raised')
        Wishlist.place(x=190, y=260)

        rectangle_32 = Frame(frame1, width=1150, height=320, bg="#282828")
        rectangle_32.place(x=100, y=470)

        description = Label(rectangle_32, text='Book Description', font=("Arial", 20, 'bold'), fg='#FFFFFF', bg="#282828")
        description.place(x=50, y=20)

        line2 = Frame(rectangle_32, width=root.winfo_screenwidth(), height=3, bg='#4F4F4F')
        line2.place(x=0, y=63)

        # Update the display with book information
        
        book_title = book.get('title', 'N/A')
        title_label = Label(rectangle_31, text=book_title, bg="#282828", fg="#FFFFFF", font=("Arial", 20))
        title_label.place(x=180, y=52)
        #title_label.config(text=book_title)
        
        authors = book['authors']
        str_authors = ', '.join(author['name'] for author in authors) if authors else 'Unknown author'  
        author_label = Label(rectangle_31, text=str_authors, bg="#282828", fg="#FFFFFF", font=("Arial", 20))
        author_label.place(x=180, y=102)
        #author_label.config(text=author_names)
        
        publishers = book.get('first_publish_year', 'N/A')
        publication_label = Label(rectangle_31, text=publishers, bg="#282828", fg="#FFFFFF", font=("Arial", 20))
        publication_label.place(x=180, y=212)
        #publication_label.config(text=', '.join(publishers))

        isbn = book['availability']['isbn']
        isbn_label = Label(rectangle_31, text=isbn, bg="#282828", fg="#FFFFFF", font=("Arial", 20))
        isbn_label.place(x=180, y=162)
        #isbn_label.config(text=isbn)
        
        description_info = fetch_book_description(book['availability']['openlibrary_work'])
        description_label = Label(rectangle_32, text=description_info['description'], bg="#282828", fg="#FFFFFF",font=("Arial", 18), wraplength=1000, justify=LEFT)
        description_label.place(x=5, y=70)
        
        # def wishlist_function(book_title,authors):
        #     for author in authors:
        #         extra.wishlist(book_title,author['name'])
        # #Wishlist.bind('Button-1>',wishlist_function(book_title,authors))
        # Wishlist.config(command=lambda: wishlist_function(book_title, authors))

        
        # def download_function(key,title):
        #     #extra.download(book_details)
        #     extra.download(key, title)
        # #Download.bind('Button-1>',download_function)
        # Download.config(command=lambda key=book_details['key'], title=book_details['title']: download_function(key, title))


        
        #Wishlist.bind('Button-1',wishlist_function)
# Retrieve and display book cover image
        cover_image_url = f"{COVER_BASE}/{book_details['cover_id']}-L.jpg"

        try:
            cover_image_response = requests.get(cover_image_url)
            cover_image_data = BytesIO(cover_image_response.content)
            image = Image.open(cover_image_data)
            image = image.resize((240, 420))  # Resize image to desired dimensions
            photo = ImageTk.PhotoImage(image)
            
            image_label = Label(frame2, image=photo, bg="#2C2F30")
            image_label.image = photo  # Retain reference to the image
            image_label.place(x=0, y=60)
            
        except Exception as e:
            print(f"Error loading image: {e}")

        root.mainloop()
        
    def fetch_book_description (openlibrary_work):
        try:
            book_details_response = requests.get(f"{API_BASE}/works/{openlibrary_work}.json")
            book_details_response.raise_for_status()
            book_details = book_details_response.json()
            return {"description": book_details['description']['value']}
        except requests.exceptions.HTTPError as err:
            print(f"HTTP error occurred: {err}")
            return {"description": "N/A"}
        except Exception as err:
            print(f"Other error occurred: {err}")
            return {"description": "N/A"}

    update_display(book_details)