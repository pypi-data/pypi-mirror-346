import os
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox

def img(object_name: str):
    """Display an offline image of a celestial object in a UI window."""
    # Normalize input
    object_name = object_name.strip().lower()

    # Path to image directory
    image_dir = os.path.join(os.path.dirname(__file__), "images")
    image_path = os.path.join(image_dir, f"{object_name}.jpg")

    if not os.path.exists(image_path):
        messagebox.showerror("Image Not Found", f"No image found for '{object_name}'.")
        return

    # Create main window
    root = tk.Tk()
    root.title(f"CosmoTalker - {object_name.title()}")

    # Load and resize image
    img = Image.open(image_path)
    img = img.resize((500, 500), Image.ANTIALIAS)
    photo = ImageTk.PhotoImage(img)

    # Create label to hold image
    label = tk.Label(root, image=photo)
    label.image = photo  # Keep reference to avoid garbage collection
    label.pack(padx=10, pady=10)

    # Label title
    name_label = tk.Label(root, text=object_name.title(), font=("Helvetica", 16, "bold"))
    name_label.pack()

    root.mainloop()

