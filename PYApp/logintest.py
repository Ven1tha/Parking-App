import bcrypt
import customtkinter
import tkinter
import webbrowser

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

root = customtkinter.CTk()
root.geometry("500x350")

def welcome():
    print("Welcome to your dashboard!")

def gainAccess():
    username = entry1.get()
    password = entry2.get()

    if not len(username or password) < 1:
        try:
            db = open("DB/logininfo.txt", "r")
            d = []
            f = []
            for i in db:
                a, b = i.split(",")
                b = b.strip()
                c = a, b
                d.append(a)
                f.append(b)
                data = dict(zip(d, f))

            if username in data:
                hashed = data[username].strip('b')
                hashed = hashed.replace("'", "")
                hashed = hashed.encode('utf-8')

                try:
                    if bcrypt.checkpw(password.encode(), hashed):
                        print("Successfully Logged In!")
                        print("Hi", username)
                        welcome()
                    else:
                        print("Incorrect password")
                except:
                    print("Incorrect password or username")
            else:
                print("This Username doesn't exist")
        except:
            print("This Username or Password doesn't exist")
    else:
        print("Please try again")

def login():
    gainAccess()

def open_signup():
    webbrowser.open_new("signup.py")

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

signup_label = tkinter.Label(master=frame, text="Don't have an account? Click Here")
signup_label.pack(pady=5)
signup_label.bind("<Button-1>", lambda event: open_signup())

root.mainloop()
