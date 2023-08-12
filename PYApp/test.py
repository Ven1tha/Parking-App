import tkinter as tk
import requests

def validate_address():
    user_input = address_entry.get()
    
    api_key = '48d389700f2947a2ac659c58350a3810'
    base_url = 'https://api.geoapify.com/v1/geocode/autocomplete'
    
    params = {
        'text': user_input,
        'apiKey': api_key
    }
    
    response = requests.get(base_url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        if data['features']:
            validated_address = data['features'][0]['properties']['formatted']
            address_entry.delete(0, tk.END)
            address_entry.insert(0, validated_address)
    else:
        print("Error fetching address data.")

# Create the Tkinter window
root = tk.Tk()
root.title("Address Validation App")

# Create and place widgets on the window
address_label = tk.Label(root, text="Enter your address:")
address_label.pack()

address_entry = tk.Entry(root)
address_entry.pack()

validate_button = tk.Button(root, text="Validate Address", command=validate_address)
validate_button.pack()

root.mainloop()
