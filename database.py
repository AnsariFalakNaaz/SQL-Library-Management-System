import sqlite3

# Connect to the SQLite database (or create it if it doesn't exist)
def create_connection():
    return sqlite3.connect('library.db')

# Create Tables
def create_tables(cursor):
    cursor.execute('DROP TABLE IF EXISTS Books')  # This will drop the table
    cursor.execute('''CREATE TABLE IF NOT EXISTS Books (
        book_id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        author TEXT NOT NULL,
        genre TEXT NOT NULL,
        published_year INTEGER,
        available_copies INTEGER NOT NULL
    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS Members (
        member_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        phone TEXT,
        membership_date TEXT NOT NULL
    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS Transactions (
        transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
        book_id INTEGER,
        member_id INTEGER,
        borrow_date TEXT NOT NULL,
        return_date TEXT,
        FOREIGN KEY (book_id) REFERENCES Books(book_id),
        FOREIGN KEY (member_id) REFERENCES Members(member_id)
    )''')
