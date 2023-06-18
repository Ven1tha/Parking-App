import bcrypt
import customtkinter
import tkinter
import webbrowser
import random

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

root = customtkinter.CTk()
root.geometry("500x350")

def open_login():
    root.destroy()
    webbrowser.open_new("login.py")

def generate_user_id():
    user_id = random.randint(1000, 9999)
    db = open("DB/logininfo.txt", "r")
    for line in db:
        if str(user_id) in line:
            return generate_user_id() 
    return str(user_id)

def register():
    username = entry1.get()
    password1 = entry2.get()
    password2 = entry3.get()

    db = open("DB/logininfo.txt", "r")
    d = []
    for i in db:
        a, b, *_ = i.split(",")
        d.append(a)

    if not len(password1) <= 3:
        db = open("DB/logininfo.txt", "r")

        if not username:
            print("Please enter a username")
            return

        if username in d:
            print("This username already exists")
            return

        if password1 == password2:
            user_id = generate_user_id()
            password1 = password1.encode('utf-8')
            hashed_password = bcrypt.hashpw(password1, bcrypt.gensalt())

            db = open("DB/logininfo.txt", "a")
            db.write(f"{user_id}, {username}, {hashed_password}\n")

            print("User created successfully!")
            print("Please log in to proceed:")

            webbrowser.open_new("login.py")
            root.destroy()

        else:
            print("Passwords do not match")
            return
    else:
        print("Password needs to be at least 4 characters long")
        return

def signup():
    register()

frame = customtkinter.CTkFrame(master=root)
frame.pack(pady=20, padx=60, fill="both", expand=True)

label = customtkinter.CTkLabel(master=frame, text="Create Account", font=("Blinker", 25))
label.pack(pady=12, padx=10)

entry1 = customtkinter.CTkEntry(master=frame, placeholder_text="Username")
entry1.pack(padx=10, pady=12)

entry2 = customtkinter.CTkEntry(master=frame, placeholder_text="Password", show="*")
entry2.pack(padx=10, pady=12)

entry3 = customtkinter.CTkEntry(master=frame, placeholder_text="Confirm Password", show="*")
entry3.pack(padx=10, pady=12)

signup_button = customtkinter.CTkButton(master=frame, text="Signup", command=signup)
signup_button.pack(pady=12, padx=10)

login_label = customtkinter.CTkLabel(master=frame, text="Already Have An Account? Click Here!", font=("Blinker", 10), cursor="hand2", fg_color="#212121")
login_label.pack(pady=1)
login_label.bind("<Button-1>", lambda event: open_login())

root.mainloop()
