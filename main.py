import tkinter as tk
from library_app import LibraryApp
from database import create_tables, create_connection

def main():
    # Create the main application window
    root = tk.Tk()
    app = LibraryApp(root)

    # Create database tables
    with create_connection() as conn:
        cursor = conn.cursor()
        create_tables(cursor)

    # Run the application
    root.mainloop()

if __name__ == "__main__":
    main()
