import tkinter as tk
from tkinter import filedialog

def select_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        folder_path_label.config(text=f"Carpeta: {folder_path}")

# Create the main window
root = tk.Tk()
root.title("Folder Selection Example")

# Create a label to display the selected folder path
folder_path_label = tk.Label(root, text="", padx=10, pady=10)
folder_path_label.pack()

# Create a button to open the folder selection dialog
select_button = tk.Button(root, text="Seleccionar Carpeta", command=select_folder)
select_button.pack()

# Start the Tkinter main loop
root.mainloop()