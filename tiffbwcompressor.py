"""module provides a way of using operating system dependent functionality"""

import os
import time
import threading
from tkinter import filedialog, StringVar
import customtkinter as ctk
from PIL import Image  # ImageTk

# Initialize the customtkinter window
app = ctk.CTk()
app.title("NMI Judiciary TIF Conv/Comp")
app.geometry("400x300")
# change application icon
# app.wm_iconbitmap()
# ICOPATH = ImageTk.PhotoImage(file="C:\\Users\\path\\to\\icon")
# app.iconphoto(False, ICOPATH)


# Variables to track progress and status
progress_var = ctk.DoubleVar()
status_var = StringVar(value="Waiting...")
file_count_var = StringVar(value="Files processed: 0")


# Function to convert TIFF files
def convert_tiff_files(input_dir, output_dir):
    """convert tiff files"""
    start_time = time.time()
    files = [f for f in os.listdir(input_dir) if f.lower().endswith(".tif")]
    total_files = len(files)
    processed_files = 0

    for file in files:
        try:
            # Open the uncompressed TIFF file
            with Image.open(os.path.join(input_dir, file)) as img:
                # check if image is multi-page
                if hasattr(img, "n_frames") and img.n_frames > 1:
                    # create a list to hold all pages
                    pages = []
                    for i in range(img.n_frames):
                        img.seek(i)
                        # convert each page to black and white and add to the list
                        pages.append(img.convert("1"))

                    # save the multi-page tif with group 4 compression
                    pages[0].save(
                        os.path.join(output_dir, file),
                        save_all=True,
                        append_images=pages[1:],
                        compression="group4",
                        dpi=(300, 300),
                    )
                else:
                    # if single page, convert to black and white and save
                    bw_img = img.convert("1")
                    bw_img.save(
                        os.path.join(output_dir, file),
                        compression="group4",
                        dpi=(300, 300),
                    )

            processed_files += 1
            progress_var.set((processed_files / total_files) * 100)
            file_count_var.set(f"Files processed: {processed_files}/{total_files}")
            status_var.set(f"Processing: {file}")
            app.update_idletasks()
        except Exception as e:
            status_var.set(f"Error: {str(e)}")

    elapsed_time = time.time() - start_time
    status_var.set(f"Completed in {elapsed_time:.2f} seconds")
    progress_var.set(100)


# Function to start the conversion process in a separate thread
def start_conversion():
    """execute conversion"""
    input_dir = filedialog.askdirectory(title="Select Input Directory")
    output_dir = filedialog.askdirectory(title="Select Output Directory")

    if input_dir and output_dir:
        threading.Thread(
            target=convert_tiff_files, args=(input_dir, output_dir)
        ).start()


# UI Elements

label = ctk.CTkLabel(
    app,
    text="NMI Judiciary TIFF Converter & Compressor",
    fg_color="transparent",
    font=("Arial", 14),
)
label.pack(pady=20, padx=20)

progress_bar = ctk.CTkProgressBar(app, variable=progress_var)
progress_bar.pack(pady=20, padx=20)

status_label = ctk.CTkLabel(app, textvariable=status_var)
status_label.pack(pady=10)

file_count_label = ctk.CTkLabel(app, textvariable=file_count_var)
file_count_label.pack(pady=10)

start_button = ctk.CTkButton(
    app, text="Select folders", font=("Arial", 16), command=start_conversion
)
start_button.pack(pady=10)

# Run the application
app.mainloop()
