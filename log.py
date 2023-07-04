import secrets
import hashlib
from tkinter import *
from tkinter import messagebox
import pymysql

def connection():
    try:
        # Establishing a connection to the database
        conn = pymysql.connect(host='localhost', user='root', password='', database='library', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)

        # Creating a cursor object using the cursor() method
        cursor = conn.cursor()

        return conn, cursor
    except pymysql.Error as e:
        print("Error connecting to database:", e)

def register(username=None, password=None):
    if username and password:
        if len(username) == 0 or len(password) == 0:
            messagebox.showinfo('ERROR', 'You have to fill the form completely')
        else:
            # Connection to the database
            conn, cur = connection()
            cur.execute("SELECT email FROM user2 WHERE email='" + username + "'")
            result = cur.fetchone()
            if result:
                messagebox.showinfo('ERROR', 'A user with this email already exists')
            else:
                salt = secrets.token_hex(16)
                hashed_password = hashlib.sha256((password + salt).encode()).hexdigest()

                cur.execute("INSERT INTO user2(name, email, password, salt) VALUES (%s, %s, %s, %s)",
                            (username, username, hashed_password, salt))
                conn.commit()
                messagebox.showinfo('SUCCESS', 'You have successfully registered')
                login()
    else:
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

        # Asking for the user to register
        # First frame containing name
        f1 = Frame(tk, height=500, width=800, bg="#2C2F30")
        f1.place(x=550, y=300)

        name_label = Label(f1, text='Name', bg="#2C2F30", fg="#FFFFFF", font=("Arial", 20, "bold"))
        name_label.place(x=0, y=0)

        e1 = Entry(f1, font=("Arial", 20))
        e1.place(x=180, y=0)

        # Second frame containing email
        f2 = Frame(tk, height=500, width=800, bg="#2C2F30")
        f2.place(x=550, y=400)

        email_label = Label(f2, text='Email', bg="#2C2F30", fg="#FFFFFF", font=("Arial", 20, "bold"))
        email_label.place(x=0, y=0)

        e2 = Entry(f2, font=("Arial", 20))
        e2.place(x=180, y=0)

        # Third frame containing password
        f3 = Frame(tk, height=500, width=800, bg="#2C2F30")
        f3.place(x=550, y=500)

        password_label = Label(f3, text='Password', bg="#2C2F30", fg="#FFFFFF", font=("Arial", 20, "bold"))
        password_label.place(x=0, y=0)

        e3 = Entry(f3, font=("Arial", 20), show='*')
        e3.place(x=180, y=0)

        # Button to validate the inputs and register the user
        register_button = Button(tk, text='Register', bg="#2C2F30", fg="#FFFFFF", font=("Arial", 16, "bold"), command=lambda: register(e2.get(), e3.get()))
        register_button.place(x=750, y=640)

        # Button to go back to the login screen
        login_button = Button(tk, text='Login', bg="#2C2F30", fg="#FFFFFF", font=("Arial", 16, "bold"), command=lambda: login(tk))
        login_button.place(x=650, y=640)

        tk.mainloop()

def login(tk=None):
    if tk:
        tk.destroy()

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

    def validate_login():
        username = e1.get()
        password = e2.get()

        # Connection to the database
        conn, cur = connection()
        cur.execute("SELECT * FROM user2 WHERE email='" + username + "'")
        result = cur.fetchone()

        if result:
            salt = result['salt']
            hashed_password = hashlib.sha256((password + salt).encode()).hexdigest()
            entered_password_hashed = hashlib.sha256((password + salt).encode()).hexdigest()

            if entered_password_hashed == result['password']:
                messagebox.showinfo('SUCCESS', 'Login Successful')
                tk.destroy()
                # Perform additional actions after successful login
            else:
                messagebox.showinfo('ERROR', 'Incorrect Password')
        else:
            messagebox.showinfo('ERROR', 'User not found')


    # Frame 1
    frame1 = Frame(tk, bg="#2C2F30")
    frame1.pack(fill=BOTH, expand=True)

    # Line 1
    line1 = Frame(frame1, width=tk.winfo_screenwidth(), height=1, bg="#4F4F4F")
    line1.place(x=0, y=63)

    # E-Lib
    elib = Label(frame1, text="E-Lib", bg="#2C2F30", fg="#FFFFFF", font=("Arial", 22, "bold"))
    elib.place(x=35, y=20)

    # Login Form
    f1 = Frame(tk, height=500, width=800, bg="#2C2F30")
    f1.place(x=550, y=400)

    email_label = Label(f1, text='Email', bg="#2C2F30", fg="#FFFFFF", font=("Arial", 20, "bold"))
    email_label.place(x=0, y=0)

    e1 = Entry(f1, font=("Arial", 20))
    e1.place(x=180, y=0)

    password_label = Label(f1, text='Password', bg="#2C2F30", fg="#FFFFFF", font=("Arial", 20, "bold"))
    password_label.place(x=0, y=80)

    e2 = Entry(f1, font=("Arial", 20), show='*')
    e2.place(x=180, y=80)

    button = Button(f1, text='Login', bg="#2C2F30", fg="#FFFFFF", font=("Arial", 16, "bold"), command=validate_login)
    button.place(x=160, y=160)

    # Button to go to the registration screen
    register_button = Button(tk, text='Register', bg="#2C2F30", fg="#FFFFFF", font=("Arial", 16, "bold"), command=lambda: register(tk))
    register_button.place(x=750, y=640)

    tk.mainloop()

# Call the login function to start the login process
login()