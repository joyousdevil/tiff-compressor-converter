# TIFF Compressor & Converter

Simple TIFF compressor that converts TIFF files to black &amp; white and compresses TIFF files using Group 4 (CCITT T.6) compression.

## Libraries

- [pillow](https://pypi.org/project/pillow/) - a python imaging library
- [tkinter](https://docs.python.org/3/library/tkinter.html) - a python library for building cross-platform GUI applications
- [customtkinter](https://customtkinter.tomschimansky.com/) - a modern and customizable python UI-library based on tkinter
- [pyinstaller](https://pyinstaller.org/en/stable/) - a tool that packages python applications and their dependencies into a single executable file

## Building the application

1. Install the libraries using pip:

   ```bash
   pip install pillow tkinter customtkinter pyinstaller
   ```

2. Build the executable:

   ```bash
   pyinstaller --noconfirm --onedir --windowed --add-data="C:\Users\<username>\path\to\site-packages\customtkinter":. .\tiffbwcompressor.py
   ```
 - Use `pip show customtkinter` to find the path to customtkinter's directory.

3. The executable will be located in `.\dist\tiffbwcompressor\`
