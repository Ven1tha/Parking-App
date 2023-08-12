import tkinter as tk
from tkinter import messagebox
import requests

# Define the Nominatim API endpoint
NOMINATIM_ENDPOINT = "https://nominatim.openstreetmap.org/search"

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

        # Validate the address
        if not validate_address(full_address):
            messagebox.showwarning("Warning", "Invalid address. Please enter a valid address.")
            return

        with open("DB/listings.txt", "a") as file:
            file.write(f"{house_number}, {street_name}, {city}\n")

        listbox_available_spaces.insert(tk.END, f"{house_number}, {street_name}, {city}")
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

    with open("DB\listings.txt", "r") as file:
        listings = file.readlines()

    selected_listing = listings.pop(selected_space).strip()

    with open("DB\listings.txt", "w") as file:
        file.writelines(listings)

    try:
        with open("DB\logininfo.txt", "r") as login_file:
            # Read the last line of the logininfo.txt file
            last_line = None
            for line in login_file:
                last_line = line.strip().split(", ")
            if last_line and len(last_line) == 3:  # Check for three pieces of information (UserID, Username, Password)
                user_id, username, _ = last_line  # Discard the password
                user_id = user_id.strip()
                username = username.strip()
            else:
                raise ValueError("Invalid format in logininfo.txt")
    except FileNotFoundError:
        messagebox.showerror("Error", "logininfo.txt not found!")
        return
    except ValueError as e:
        messagebox.showerror("Error", str(e))
        return

    with open("DB/bookings.txt", "a") as bookings_file:
        bookings_file.write(f"{user_id}, {username}, {selected_listing}\n")

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

    with open("DB\listings.txt", "r") as file:
        listings = file.readlines()

    for listing in listings:
        listbox_available_spaces.insert(tk.END, listing.strip())

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
