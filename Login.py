from tkinter import *
from tkinter import messagebox
import secrets
import hashlib
import pymysql

# Creating list for user info
global user

class UserManager:

    def __init__(self):
        self.name = "Placeholder"
        self.email = "Placeholder"
        self.islogged = False

    def update_details(self, user_details):
        self.name = user_details['name']
        self.email = user_details['email']
        self.islogged = True
        return self.get_user_info()
    
    def get_user_info(self):
        return {
            "name": self.name,
            "email": self.email
        }


user = UserManager()


def connection():
    try:
        # Establishing a connection to the database
        conn = pymysql.connect(host='localhost', user='root', password='', database='library', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)

        # Creating a cursor object using the cursor() method
        cursor = conn.cursor()

        return conn, cursor
    except pymysql.Error as e:
        print("Error connecting to database:", e)


def register(username=None, email=None, password=None):
    if username and email and password:
        if len(username) == 0 or len(email) == 0 or len(password) == 0:
            messagebox.showinfo('ERROR', 'You have to fill the form completely')
        else:
            # Connection to the database
            conn, cur = connection()
            cur.execute("SELECT email FROM user2 WHERE email='" + email + "'")
            result = cur.fetchone()
            if result:
                messagebox.showinfo('ERROR', 'A user with this email already exists')
            else:
                salt = secrets.token_hex(16)
                hashed_password = hashlib.sha256((password + salt).encode()).hexdigest()

                cur.execute("INSERT INTO user2 (name, email, password, salt) VALUES (%s, %s, %s, %s)", (username, email, hashed_password, salt))
                conn.commit()
                messagebox.showinfo('SUCCESS', 'You have successfully registered')
                conn.close()
                tk.destroy()
                # Call the login function or perform any other desired action
                login()
    else:
        # First connection recall so that I get a window in case of an error.
        connection()

        # Creating the main theme
        tk = Tk()
        tk.state('zoomed')
        tk.configure(background='#2C2F30')

        # Set user_data to None to reset its contents
        global user_data
        user_data.clear()

        # Get the screen width and height
        screen_width = tk.winfo_screenwidth()
        screen_height = tk.winfo_screenheight()

        # Center the login interface on the screen
        window_width = 400
        window_height = 250
        x_position = (screen_width - window_width) // 2
        y_position = (screen_height - window_height) // 2
        tk.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

        # Frame 1
        frame1 = Frame(tk, bg="#2C2F30")
        frame1.pack(fill=BOTH, expand=True)

        # Line 1
        line1 = Frame(frame1, width=tk.winfo_screenwidth(), height=1, bg="#4F4F4F")
        line1.place(x=0, y=63)

        # E-Lib
        elib = Label(frame1, text="E-Lib", bg="#2C2F30", fg="#FFFFFF", font=("Arial", 22, "bold"))
        elib.place(x=35, y=20)

        # Asking for the user to register
        # First frame containing name
        f1 = Frame(tk, height=500, width=800, bg="#2C2F30")
        f1.place(x=550, y=300)

        name_label = Label(f1, text='Name', bg="#2C2F30", fg="#FFFFFF", font=("Arial", 20, "bold"))
        name_label.place(x=0, y=0)

        e1 = Entry(f1, font=("Arial", 20))
        e1.place(x=170, y=0)

        # Second frame containing email
        f2 = Frame(tk, height=500, width=800, bg="#2C2F30")
        f2.place(x=550, y=370)

        email_label = Label(f2, text='Email', bg="#2C2F30", fg="#FFFFFF", font=("Arial", 20, "bold"))
        email_label.place(x=0, y=0)

        e2 = Entry(f2, font=("Arial", 20))
        e2.place(x=170, y=0)

        # Third frame containing password
        f3 = Frame(tk, height=500, width=800, bg="#2C2F30")
        f3.place(x=550, y=440)

        passwo = Label(f3, text='Password', bg="#2C2F30", fg="#FFFFFF", font=("Arial", 20, "bold"))
        passwo.place(x=0, y=0)

        e3 = Entry(f3, show='*', font=("Arial", 20))
        e3.place(x=170, y=0)

        # Submit button
        b1 = Button(tk, text='Register', font=("Arial", 15), bg='#61dfdd', padx=34, pady=8, command=lambda: register(e1.get(), e2.get(), e3.get()))
        b1.place(x=850, y=530)

        # Login button
        b2 = Button(tk, text='Login', font=("Arial", 15), bg='#61dfdd', padx=34, pady=8, command=login)
        b2.place(x=550, y=530)

        tk.mainloop()


def login(event):
    def authenticate():
        conn, cur = connection()

        query = "SELECT name, email, password, salt FROM user2 WHERE email=%s"
        cur.execute(query, (e2.get()))

        result = cur.fetchone()

        cur.close()
        conn.close()

        if result:
            salt = result['salt']
            entered_password_hashed = hashlib.sha256((e3.get() + salt).encode()).hexdigest()
            if entered_password_hashed == result['password']:
                messagebox.showinfo('Success', 'Logged in successfully!')
                response = user.update_details(result)
                print(response)
                tk.destroy()
            else:
                messagebox.showerror('Error', 'Invalid email or password!')
        else:
            messagebox.showerror('Error', 'Invalid email or password!')

    # First connection recall so that I get a window in case of an error.
    connection()

    # Creating the main theme
    tk = Tk()
    tk.state('zoomed')
    tk.configure(background='#2C2F30')

    # Get the screen width and height
    screen_width = tk.winfo_screenwidth()
    screen_height = tk.winfo_screenheight()

    # Center the login interface on the screen
    window_width = 400
    window_height = 250
    x_position = (screen_width - window_width) // 2
    y_position = (screen_height - window_height) // 2
    tk.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

    # Frame 1
    frame1 = Frame(tk, bg="#2C2F30")
    frame1.pack(fill=BOTH, expand=True)

    # Line 1
    line1 = Frame(frame1, width=tk.winfo_screenwidth(), height=1, bg="#4F4F4F")
    line1.place(x=0, y=63)

    # E-Lib
    elib = Label(frame1, text="E-Lib", bg="#2C2F30", fg="#FFFFFF", font=("Arial", 22, "bold"))
    elib.place(x=35, y=20)

    # First frame containing email
    f1 = Frame(tk, height=500, width=800, bg="#2C2F30")
    f1.place(x=550, y=300)

    email_label = Label(f1, text='Email', bg="#2C2F30", fg="#FFFFFF", font=("Arial", 20, "bold"))
    email_label.place(x=0, y=0)

    e2 = Entry(f1, font=("Arial", 20))
    e2.place(x=170, y=0)

    # Second frame containing password
    f2 = Frame(tk, height=500, width=800, bg="#2C2F30")
    f2.place(x=550, y=370)

    passwo = Label(f2, text='Password', bg="#2C2F30", fg="#FFFFFF", font=("Arial", 20, "bold"))
    passwo.place(x=0, y=0)

    e3 = Entry(f2, show='*', font=("Arial", 20))
    e3.place(x=170, y=0)

    # Submit button
    b1 = Button(tk, text='Login', font=("Arial", 15), bg='#61dfdd', padx=34, pady=8, command=authenticate)
    b1.place(x=850, y=530)

    # Register button
    b2 = Button(tk, text='Register', font=("Arial", 15), bg='#61dfdd', padx=34, pady=8, command=register)
    b2.place(x=550, y=530)

    tk.mainloop()




if __name__ == '__main__':
    login(event=None)
