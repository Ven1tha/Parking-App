import bcrypt
import customtkinter
import tkinter

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

def register():
    username = entry1.get()
    password1 = entry2.get()
    password2 = entry2.get()
    
    db = open("DB/logininfo.txt", "r")
    d = []
    for i in db:
        a, b = i.split(",")
        b = b.strip()
        c = a, b
        d.append(a)
    
    if not len(password1) <= 3:
        db = open("DB/logininfo.txt", "r")
        
        if not username == None:
            if len(username) < 1:
                print("Please enter a username")
                return
                        
            elif username in d:
                print("This Username exists")
                return
            
            else:
                if password1 == password2:
                    password1 = password1.encode('utf-8')
                    hashed_password = bcrypt.hashpw(password1, bcrypt.gensalt())
                    
                    db = open("DB/logininfo.txt", "a")
                    db.write(username + ", " + str(hashed_password) + "\n")
                    
                    print("User created successfully!")
                    print("Please login to proceed:")
                    
                else:
                    print("Passwords do not match")
                    return
    else:
        print("Password needs to be at least 4 characters long")
        return

def login():
    gainAccess()

def signup():
    register()

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

signup_button = customtkinter.CTkButton(master=frame, text="Signup", command=signup)
signup_button.pack(pady=12, padx=10)

root.mainloop()
