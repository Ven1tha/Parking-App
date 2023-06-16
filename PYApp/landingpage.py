import tkinter as tk
from tkinter import ttk
import subprocess
from PIL import ImageTk, Image

def open_next_page():
    #Closes the old window before opening a new one
    window.destroy()

    # Function to handle button click and navigate to the next page
    subprocess.run(['python', 'login.py'])
    pass

# Create the main window
window = tk.Tk()

# Set window properties
window.title("Python App Landing")
window.geometry("800x600")  # Set the desired window size

# Load the background image
image = Image.open("Assets/landingimage.jpg")
image = image.resize((800, 600), Image.LANCZOS) # Resize the image to fit the window
background_image = ImageTk.PhotoImage(image)

# Create a canvas to place the image and overlay
canvas = tk.Canvas(window, width=800, height=600)
canvas.pack(fill="both", expand=True)

# Display the background image
canvas.create_image(0, 0, image=background_image, anchor="nw")

# Add text overlay
text = canvas.create_text(400, 200, text="Parking Solutions", font=("Arial", 30, 'bold'), fill="white", justify="center")

# Create a style for the button
style = ttk.Style()
style.configure("TButton", foreground="black", background="#0390fc", font=("Heebo", 14), width=20)

# Create the button
button = ttk.Button(window, text="Login", command=open_next_page, style="TButton")
button_window = canvas.create_window(400, 400, anchor="center", window=button)

window.mainloop()
