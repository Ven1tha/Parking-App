import bcrypt
import customtkinter
import tkinter as tk
import webbrowser

#sets the background of the login page to black
customtkinter.set_appearance_mode("dark")
#sets the buttons within the page to blue
customtkinter.set_default_color_theme("dark-blue")

root = customtkinter.CTk()
root.geometry("500x350")

def open_home():
    print("Welcome To Parking Solutions!")

'''setting username and password fields'''
def gainAccess():
    username = entry1.get().lower()
    password = entry2.get()

    if not len(username or password) < 1:
        try:
            db = open("PYApp\DB\logininfo.txt", "r")
            for i in db:
                user_id, stored_username, stored_password = i.strip().split(", ")
                if stored_username.lower() == username:
                    stored_password = stored_password[2:-1]
                    stored_password = stored_password.encode('utf-8')
                    if bcrypt.checkpw(password.encode('utf-8'), stored_password):
                        print("Successfully Logged In!")
                        print("Hi", stored_username)
                        open_home()
                        return 

            print("Incorrect Username Or Password")
        except:
            print("Incorrect Password")
    else:
        print("Please Try Again")

def login():
    gainAccess()

#opens the signup.py file
def open_signup():
    root.destroy()
    webbrowser.open_new("signup.py")

#GUI
frame = customtkinter.CTkFrame(master=root)
frame.pack(pady=20, padx=60, fill="both", expand=True)

label = customtkinter.CTkLabel(master=frame, text="Welcome!", font=("Blinker", 25))
label.pack(pady=12, padx=10)

entry1 = customtkinter.CTkEntry(master=frame, placeholder_text="Username")
entry1.pack(padx=10, pady=12)

entry2 = customtkinter.CTkEntry(master=frame, placeholder_text="Password", show="*")
entry2.pack(padx=10, pady=12)

login_button = customtkinter.CTkButton(master=frame, text="Login", command=login)
login_button.pack(pady=12, padx=10)

#button allows users to easily navigate to the signup page if they don't have an account
signup_label = customtkinter.CTkLabel(master=frame, text="Don't have an account? Click Here!", font=("Blinker", 10), cursor="hand2", fg_color="#212121")
signup_label.pack(pady=5)
signup_label.bind("<Button-1>", lambda event: open_signup())

root.mainloop()
