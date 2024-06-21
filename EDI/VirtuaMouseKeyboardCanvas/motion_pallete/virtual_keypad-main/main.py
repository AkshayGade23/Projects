import tkinter as tk
from tkinter import ttk
import subprocess


def on_virtual_keyboard_mouse_click():
    print("Virtual Keyboard & Mouse button clicked!")
    subprocess.run(["python", "virtual keyboard.py"])


def on_virtual_canvas_click():
    print("Virtual Canvas button clicked!")
    subprocess.run(["python", "app7.py"])


root = tk.Tk()
root.title("Motion Palette Suite")

# Set the window dimensions
window_width = 300
window_height = 300

# Get the screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Calculate the x and y coordinates for the Tk root window
x = (screen_width / 2) - (window_width / 2)
y = (screen_height / 2) - (window_height / 2)

# Set the dimensions of the screen and where it is placed
root.geometry('%dx%d+%d+%d' % (window_width, window_height, x, y))

# Set the window background to black
root.configure(bg="black")

# Create a style for the buttons
style = ttk.Style()
style.configure('TButton', background='grey', foreground='black')

# Create a label for the title
title_label = tk.Label(root, text="Motion Palette Suite", font=("Helvetica", 16), bg="black", fg="white")
title_label.pack(pady=10)

# Create a button for Virtual Keyboard & Mouse
keyboard_mouse_button = ttk.Button(root, text="Virtual Keyboard & Mouse", command=on_virtual_keyboard_mouse_click, style="TButton")
keyboard_mouse_button.pack(pady=10)

# Create a button for Virtual Canvas
canvas_button = ttk.Button(root, text="Virtual Canvas", command=on_virtual_canvas_click, style="TButton")
canvas_button.pack(pady=10)

# Run the Tkinter event loop
root.mainloop()
