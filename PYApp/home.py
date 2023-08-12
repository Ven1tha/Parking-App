import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# Create the main application window
app = tk.Tk()

# Set the window title
app.title("Home")

# Set the background color to blue
app.configure(background="blue")

# Create the tabs for listing and booking a parking space
tabs = ttk.Notebook(app)

# Create the tab for listing a parking space
list_tab = ttk.Frame(tabs)

# Create the form for listing a parking space
list_frame = ttk.Frame(list_tab, padding=50)
list_frame.pack()

# Street Name input
street_label = ttk.Label(list_frame, text="Street Name:")
street_label.pack()
street_entry = ttk.Entry(list_frame)
street_entry.pack()

# City input
city_label = ttk.Label(list_frame, text="City:")
city_label.pack()
city_entry = ttk.Entry(list_frame)
city_entry.pack()

def submit_listing():
    street = street_entry.get()
    city = city_entry.get()
    with open("DB\listings.txt", "a") as file:
        file.write(f"{street},{city}\n")
    messagebox.showinfo("Listing Successful", "Parking space has been listed.")
    street_entry.delete(0, tk.END)
    city_entry.delete(0, tk.END)
    populate_listbox()  # Refresh the listbox after listing

# Submit button for listing a parking space
submit_button = ttk.Button(list_frame, text="Submit", command=submit_listing)
submit_button.pack(pady=10)

# Add the listing tab to the tabs
tabs.add(list_tab, text="List Parking Space")

# Create the tab for booking a parking space
book_tab = ttk.Frame(tabs)

# Create a listbox for displaying available parking spaces
listbox = tk.Listbox(book_tab, width=50)
listbox.pack(pady=10)

def populate_listbox():
    listbox.delete(0, tk.END)
    with open("DB\listings.txt", "r") as file:
        lines = file.readlines()
        for line in lines:
            street, city = line.strip().split(',')
            listbox.insert(tk.END, f"{street} - {city}")

populate_listbox()

def book_space():
    selected_indices = listbox.curselection()
    if selected_indices:
        selected_items = [listbox.get(index) for index in selected_indices]

        # Read the contents of listings.txt into a list
        with open("DB\listings.txt", "r") as file:
            lines = file.readlines()

        # Create a new list with remaining parking spaces
        remaining_listings = [line.strip() for line in lines if line.strip() not in selected_items]

        # Update the listings.txt file with the new list
        with open("DB\listings.txt", "w") as file:
            file.write("\n".join(remaining_listings))

        # Remove the parking space from the listbox
        for index in selected_indices[::-1]:
            listbox.delete(index)

        # Ask for name and duration
        booking_window = tk.Toplevel(app)
        booking_window.title("Book Parking Space")
        booking_window.configure(background="blue")

        first_name_label = ttk.Label(booking_window, text="First Name:")
        first_name_label.pack()
        first_name_entry = ttk.Entry(booking_window)
        first_name_entry.pack()

        last_name_label = ttk.Label(booking_window, text="Last Name:")
        last_name_label.pack()
        last_name_entry = ttk.Entry(booking_window)
        last_name_entry.pack()

        duration_label = ttk.Label(booking_window, text="Duration (in hours):")
        duration_label.pack()
        duration_entry = ttk.Entry(booking_window)
        duration_entry.pack()

        def submit_booking():
            first_name = first_name_entry.get()
            last_name = last_name_entry.get()
            duration = duration_entry.get()
            with open("DB/bookings.txt", "a") as file:
                file.write(f"{', '.join(selected_items)},{first_name},{last_name},{duration}\n")
            messagebox.showinfo("Booking Successful", "Parking space has been booked.")
            booking_window.destroy()

        submit_button = ttk.Button(booking_window, text="Submit", command=submit_booking)
        submit_button.pack(pady=10)

    else:
        messagebox.showwarning("No Parking Space Selected", "Please select a parking space.")

# Submit button for booking a parking space
book_button = ttk.Button(book_tab, text="Book", command=book_space)
book_button.pack(pady=10)

# Add the booking tab to the tabs
tabs.add(book_tab, text="Book Parking Space")

# Pack the tabs
tabs.pack(expand=True, fill='both')

# Run the app
app.mainloop()
