import tkinter as tk
from tkinter import messagebox
import requests
from cryptography.fernet import Fernet

# Define the Nominatim API endpoint
NOMINATIM_ENDPOINT = "https://nominatim.openstreetmap.org/search"

# Define the file for encryption key storage
ENCRYPTION_KEY_FILE = "encryption_key.key"

def load_encryption_key():
    try:
        with open(ENCRYPTION_KEY_FILE, "rb") as key_file:
            return key_file.read()
    except FileNotFoundError:
        return None

def save_encryption_key(key):
    with open(ENCRYPTION_KEY_FILE, "wb") as key_file:
        key_file.write(key)

def generate_or_load_encryption_key():
    loaded_key = load_encryption_key()
    if loaded_key:
        return loaded_key
    else:
        new_key = Fernet.generate_key()
        save_encryption_key(new_key)
        return new_key

encryption_key = generate_or_load_encryption_key()
cipher_suite = Fernet(encryption_key)

def encrypt(text):
    return cipher_suite.encrypt(text.encode()).decode()

def decrypt(encrypted_text):
    return cipher_suite.decrypt(encrypted_text.encode()).decode()

def read_listings():
    listings = []
    with open("DB/listings.txt", "r") as file:
        for line in file:
            try:
                key, encrypted_listing = line.strip().split(",", 1)
                if key == encryption_key.decode():
                    decrypted_listing = decrypt(encrypted_listing)
                    listings.append(decrypted_listing)
            except Exception as e:
                print(f"Error decrypting listing: {e}")
                # Handle decryption errors here
    return listings

def autocomplete_address(input_text):
    params = {
        "format": "json",
        "q": input_text
    }
    response = requests.get(NOMINATIM_ENDPOINT, params=params)
    data = response.json()
    suggestions = [result["display_name"] for result in data]
    return suggestions

def validate_address(address):
    params = {
        "format": "json",
        "q": address
    }
    response = requests.get(NOMINATIM_ENDPOINT, params=params)
    data = response.json()
    return len(data) > 0

def list_parking_space():
    global entry_house_number, entry_street_name, entry_city, listbox_available_spaces

    house_number = entry_house_number.get()
    street_name = entry_street_name.get()
    city = entry_city.get()

    if house_number and street_name and city:
        full_address = f"{house_number}, {street_name}, {city}"

        # Check if the address is already listed
        if full_address in listbox_available_spaces.get(0, tk.END):
            messagebox.showwarning("Warning", "This address is already listed.")
            return

        # Validate the address
        if not validate_address(full_address):
            messagebox.showwarning("Warning", "Invalid address. Please enter a valid address.")
            return

        encrypted_address = encrypt(full_address)

        with open("DB/listings.txt", "a") as file:
            file.write(f"{encryption_key.decode()},{encrypted_address}\n")

        listbox_available_spaces.insert(tk.END, decrypt(encrypted_address))
        entry_house_number.delete(0, tk.END)
        entry_street_name.delete(0, tk.END)
        entry_city.delete(0, tk.END)

        messagebox.showinfo("Success", "Parking space listed successfully!")
    else:
        messagebox.showwarning("Warning", "Please fill in all the fields!")

def book_parking_space():
    global listbox_available_spaces

    selected_space = listbox_available_spaces.curselection()

    if not selected_space:
        messagebox.showwarning("Warning", "Please select a parking space!")
        return

    selected_space = selected_space[0]

    with open("DB/listings.txt", "r") as file:
        listings = file.readlines()

    selected_listing = listings.pop(selected_space).strip()

    try:
        with open("DB/current_user.txt", "r") as current_user_file:
            user_id, username = current_user_file.read().strip().split(", ")
    except FileNotFoundError:
        messagebox.showerror("Error", "current_user.txt not found!")
        return
    except ValueError:
        messagebox.showerror("Error", "Invalid format in current_user.txt")
        return

    encrypted_selected_listing = encrypt(selected_listing)

    with open("DB/bookings.txt", "a") as bookings_file:
        bookings_file.write(f"{user_id}, {username}, {encrypted_selected_listing}\n")

    with open("DB/listings.txt", "w") as listings_file:
        for listing in listings:
            listings_file.write(listing)

    listbox_available_spaces.delete(selected_space)

    messagebox.showinfo("Success", "Parking space booked successfully!")

def create_home_page():
    global entry_house_number, entry_street_name, entry_city, listbox_available_spaces

    home_page = tk.Tk()
    home_page.title("Home Page")
    
    label_heading = tk.Label(home_page, text="Home Page", font=("Helvetica", 20))
    label_heading.pack(pady=10)

    frame_list_parking = tk.Frame(home_page)
    frame_list_parking.pack(pady=10)

    label_house_number = tk.Label(frame_list_parking, text="House Number:")
    label_house_number.grid(row=0, column=0)
    entry_house_number = tk.Entry(frame_list_parking)
    entry_house_number.grid(row=0, column=1)

    label_street_name = tk.Label(frame_list_parking, text="Street Name:")
    label_street_name.grid(row=1, column=0)
    entry_street_name = tk.Entry(frame_list_parking)
    entry_street_name.grid(row=1, column=1)

    label_city = tk.Label(frame_list_parking, text="City:")
    label_city.grid(row=2, column=0)
    entry_city = tk.Entry(frame_list_parking)
    entry_city.grid(row=2, column=1)

    button_list_parking = tk.Button(frame_list_parking, text="List Parking Space", command=list_parking_space)
    button_list_parking.grid(row=3, column=0, columnspan=2, pady=10)

    frame_book_parking = tk.Frame(home_page)
    frame_book_parking.pack(pady=10)

    label_available_spaces = tk.Label(frame_book_parking, text="Available Parking Spaces:")
    label_available_spaces.pack()

    scrollbar_available_spaces = tk.Scrollbar(frame_book_parking)
    scrollbar_available_spaces.pack(side=tk.RIGHT, fill=tk.Y)

    listbox_available_spaces = tk.Listbox(frame_book_parking, yscrollcommand=scrollbar_available_spaces.set)
    listbox_available_spaces.pack(fill=tk.BOTH, expand=True)

    listings = read_listings()
    for listing in listings:
        listbox_available_spaces.insert(tk.END, listing)

    scrollbar_available_spaces.config(command=listbox_available_spaces.yview)

    button_book_parking = tk.Button(frame_book_parking, text="Book Parking Space", command=book_parking_space)
    button_book_parking.pack(pady=10)

    home_page.mainloop()

def main():
    root = tk.Tk()
    root.withdraw()  # Hide the main root window

    # Explicitly create and open the home page as the main application window
    create_home_page()

    root.mainloop()

if __name__ == "__main__":
    main()
