from tkinter import *
from tkinter import font
from pystray import MenuItem as item
import pystray
from PIL import Image, ImageTk
import serial
import time
import requests

# Global variables
global color1, color2, url
jsonblobid = "0123456789012345678"
url = f"https://jsonblob.com/api/jsonBlob/{jsonblobid}"
data = requests.get(url).json()

color1 = data.get("color1", "")
color2 = data.get("color2", "")

port = 'COM3'
baudrate = 9600
ser = serial.Serial(port, baudrate, timeout=1)
time.sleep(2)


def update_colors(num, color):
    global color1, color2
    if num == 1:
        color1 = color
    elif num == 2:
        color2 = color
    send_command()
    headers = {"Content-Type": "application/json", }
    data = {"color1": color1, "color2": color2}
    response = requests.put(url, json=data, headers=headers)


def send_command():
    try:
        # Send data to Arduino
        output = f"{color1} {color2}\n"
        ser.write(output.encode('utf-8'))
    except serial.SerialException as e:
        print(f"Error: {e}")


def quit_window(icon, item):
    icon.stop()
    win.destroy()


def show_window(icon, item):
    icon.stop()
    win.after(0, win.deiconify())


def hide_window():
    win.withdraw()
    image = Image.open("favicon.ico")
    menu = (item('Quit', quit_window), item('Show', show_window))
    icon = pystray.Icon("name", image, "LED Settings", menu)
    icon.run()


def show_color_popup(color_name):
    color = color_name.lower()
    popup = Toplevel(win)
    popup.title(f"Color: {color_name}")
    popup.geometry("200x200")
    popup.configure(bg=color)

    # Move the text close to the top
    label = Label(popup, text=f"{color_name}", font=("Helvetica", 12, "bold"),
                  fg="white" if color_name.lower() == 'black' else 'black', bg=color)
    label.pack(side=TOP, pady=5)

    # Add two buttons next to each other
    button1 = Button(popup, text="Color 1", font=("Helvetica", 10, "bold"),
                     borderwidth=0, highlightthickness=0, bg="#000000" if color_name.lower() != 'black' else 'white',
                     fg="white" if color_name.lower() != 'black' else 'black', width=8, height=2,
                     command=lambda: (update_colors(1, color_name), popup.destroy()))
    button1.pack(side=TOP, pady=10)

    button2 = Button(popup, text="Color 2", font=("Helvetica", 10, "bold"),
                     borderwidth=0, highlightthickness=0, bg="#000000" if color_name.lower() != 'black' else 'white',
                     fg="white" if color_name.lower() != 'black' else 'black', width=8, height=2,
                     command=lambda: (update_colors(2, color_name), popup.destroy()))
    button2.pack(side=TOP, pady=10)

    # Add a back button
    back_button = Button(popup, text="Back", font=("Helvetica", 10, "bold"),
                         borderwidth=0, highlightthickness=0, command=popup.destroy)
    back_button.pack(side=TOP, pady=10)

# Combined color names list
color_names = [
    "Red", "Orange", "Yellow", "Green", "Blue",
    "Purple", "Pink", "Brown", "Gray", "Black",
    "White", "Cyan", "Turquoise", "Maroon", "Lavender",
    "Beige", "Navy", "Olive", "Salmon", "Coral"
]

win = Tk()
win.title("LED Settings")
win.geometry("700x350")

# Set the Tkinter window icon to "favicon.ico"
win.iconbitmap("favicon.ico")

# Create buttons with colors
buttons = []
for i, color_name in enumerate(color_names):
    color = color_name.lower()  # Assuming color names are lowercase
    text_color = 'white' if color_name.lower() == 'black' else 'black'

    # Create a bold font
    bold_font = font.Font(family="Helvetica", size=10, weight="bold")

    # Function to handle button click
    def button_click_handler(c=color_name):
        show_color_popup(c)

    button = Button(win, text=color_name, font=bold_font, borderwidth=0, highlightthickness=0,
                    bg=color, fg=text_color, command=button_click_handler)
    buttons.append(button)

# Set up the grid to make buttons auto-resize
for i, button in enumerate(buttons):
    button.grid(row=i // 5, column=i % 5, sticky="nsew", padx=2, pady=2)  # Adjust padx and pady as needed

# Set up resizing behavior
for i in range(5):
    win.grid_columnconfigure(i, weight=1)
    win.grid_rowconfigure(i, weight=1)

# Remove the gap at the bottom
win.grid_rowconfigure(len(color_names) // 5, weight=0)

send_command()
hide_window()
win.protocol('WM_DELETE_WINDOW', hide_window)
win.mainloop()
