import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime
from database import create_connection
from email_utils import is_valid_email

class LibraryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Library Management System")
        self.root.geometry("800x600")  # Set the window size
        self.root.configure(bg="#f0f0f0")  # Set background color
        self.create_widgets()

    def create_widgets(self):
        # Heading
        self.heading_label = tk.Label(self.root, text="Library Management System", 
                                       font=("Arial", 24), bg="#4a90e2", fg="white", pady=10)
        self.heading_label.pack(fill="x")

        # Navigation Bar (Navbar)
        self.navbar_frame = tk.Frame(self.root, bg="#4a90e2")
        self.navbar_frame.pack(fill="x")

        self.book_button = tk.Button(self.navbar_frame, text="Manage Books", font=("Arial", 12), 
                                     command=self.show_books_tab, bg="#3498db", fg="white", padx=20, pady=5)
        self.book_button.grid(row=0, column=0, padx=10)

        self.member_button = tk.Button(self.navbar_frame, text="Manage Members", font=("Arial", 12), 
                                       command=self.show_members_tab, bg="#3498db", fg="white", padx=20, pady=5)
        self.member_button.grid(row=0, column=1, padx=10)

        self.transaction_button = tk.Button(self.navbar_frame, text="Transactions", font=("Arial", 12), 
                                            command=self.show_transactions_tab, bg="#3498db", fg="white", padx=20, pady=5)
        self.transaction_button.grid(row=0, column=2, padx=10)

        # Content Frame
        self.content_frame = tk.Frame(self.root, bg="#f0f0f0", pady=10)
        self.content_frame.pack(fill="both", expand=True)

        # Notebook for tabs
        self.notebook = ttk.Notebook(self.content_frame)
        self.notebook.pack(padx=10, pady=10, fill='both', expand=True)

        # Book Management Tab
        self.book_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.book_tab, text="Manage Books")
        self.create_book_widgets()

        # Member Management Tab
        self.member_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.member_tab, text="Manage Members")
        self.create_member_widgets()

        # Transaction Tab
        self.transaction_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.transaction_tab, text="Transactions")
        self.create_transaction_widgets()

    # Navigation Bar Functions
    def show_books_tab(self):
        self.notebook.select(self.book_tab)

    def show_members_tab(self):
        self.notebook.select(self.member_tab)

    def show_transactions_tab(self):
        self.notebook.select(self.transaction_tab)
        self.refresh_transactions_list()  # Refresh transactions when showing this tab

    def create_book_widgets(self):
        ttk.Label(self.book_tab, text="Title:").grid(row=0, column=0, sticky='e', padx=5, pady=5)
        self.book_title_entry = ttk.Entry(self.book_tab)
        self.book_title_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.book_tab, text="Author:").grid(row=1, column=0, sticky='e', padx=5, pady=5)
        self.book_author_entry = ttk.Entry(self.book_tab)
        self.book_author_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self.book_tab, text="Genre:").grid(row=2, column=0, sticky='e', padx=5, pady=5)
        self.book_genre_entry = ttk.Entry(self.book_tab)
        self.book_genre_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(self.book_tab, text="Published Year:").grid(row=3, column=0, sticky='e', padx=5, pady=5)
        self.book_year_entry = ttk.Entry(self.book_tab)
        self.book_year_entry.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(self.book_tab, text="Available Copies:").grid(row=4, column=0, sticky='e', padx=5, pady=5)
        self.book_copies_entry = ttk.Entry(self.book_tab)
        self.book_copies_entry.grid(row=4, column=1, padx=5, pady=5)

        ttk.Button(self.book_tab, text="Add Book", command=self.add_book).grid(row=5, columnspan=2, pady=10)

        # Entry for Book ID to delete
        ttk.Label(self.book_tab, text="Book ID to Delete:").grid(row=6, column=0, sticky='e', padx=5, pady=5)
        self.delete_book_id_entry = ttk.Entry(self.book_tab)
        self.delete_book_id_entry.grid(row=6, column=1, padx=5, pady=5)

        ttk.Button(self.book_tab, text="Delete Book", command=self.delete_book).grid(row=7, columnspan=2, pady=10)

        # Treeview to display books
        self.books_tree = ttk.Treeview(self.book_tab, columns=("ID", "Title", "Author", "Genre", "Year", "Copies"), show="headings")
        self.books_tree.heading("ID", text="ID")
        self.books_tree.heading("Title", text="Title")
        self.books_tree.heading("Author", text="Author")
        self.books_tree.heading("Genre", text="Genre")
        self.books_tree.heading("Year", text="Published Year")
        self.books_tree.heading("Copies", text="Available Copies")
        self.books_tree.grid(row=8, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

        # Ensure the treeview expands
        self.book_tab.grid_rowconfigure(8, weight=1)
        self.book_tab.grid_columnconfigure(1, weight=1)

        self.refresh_books_list()

    def refresh_books_list(self):
        # Clear the treeview first
        for row in self.books_tree.get_children():
            self.books_tree.delete(row)

        # Fetch all books from the database
        with create_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Books")
            books = cursor.fetchall()

        # Insert books into the treeview
        for book in books:
            self.books_tree.insert("", "end", values=book)

    def add_book(self):
        title = self.book_title_entry.get()
        author = self.book_author_entry.get()
        genre = self.book_genre_entry.get()
        published_year = self.book_year_entry.get()
        available_copies = self.book_copies_entry.get()

        if not title or not author or not genre or not available_copies:
            messagebox.showerror("Error", "All fields must be filled out.")
            return

        if not published_year.isdigit():
            messagebox.showerror("Error", "Published Year must be a number.")
            return

        if not available_copies.isdigit():
            messagebox.showerror("Error", "Available Copies must be a number.")
            return

        with create_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO Books (title, author, genre, published_year, available_copies) VALUES (?, ?, ?, ?, ?)",
                           (title, author, genre, int(published_year), int(available_copies)))
            conn.commit()

        self.refresh_books_list()
        messagebox.showinfo("Success", "Book added successfully!")
        self.clear_book_fields()

    def clear_book_fields(self):
        self.book_title_entry.delete(0, tk.END)
        self.book_author_entry.delete(0, tk.END)
        self.book_genre_entry.delete(0, tk.END)
        self.book_year_entry.delete(0, tk.END)
        self.book_copies_entry.delete(0, tk.END)

    def delete_book(self):
        book_id = self.delete_book_id_entry.get()
        if not book_id.isdigit():
            messagebox.showerror("Error", "Book ID must be a number.")
            return

        with create_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Books WHERE book_id = ?", (int(book_id),))
            conn.commit()

        self.refresh_books_list()
        messagebox.showinfo("Success", "Book deleted successfully!")
        self.delete_book_id_entry.delete(0, tk.END)

    def create_member_widgets(self):
        # Member management UI code here
        ttk.Label(self.member_tab, text="Name:").grid(row=0, column=0, sticky='e', padx=5, pady=5)
        self.member_name_entry = ttk.Entry(self.member_tab)
        self.member_name_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.member_tab, text="Email:").grid(row=1, column=0, sticky='e', padx=5, pady=5)
        self.member_email_entry = ttk.Entry(self.member_tab)
        self.member_email_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self.member_tab, text="Phone:").grid(row=2, column=0, sticky='e', padx=5, pady=5)
        self.member_phone_entry = ttk.Entry(self.member_tab)
        self.member_phone_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Button(self.member_tab, text="Add Member", command=self.add_member).grid(row=3, columnspan=2, pady=10)

        # Entry for Member ID to delete
        ttk.Label(self.member_tab, text="Member ID to Delete:").grid(row=4, column=0, sticky='e', padx=5, pady=5)
        self.delete_member_id_entry = ttk.Entry(self.member_tab)
        self.delete_member_id_entry.grid(row=4, column=1, padx=5, pady=5)

        ttk.Button(self.member_tab, text="Delete Member", command=self.delete_member).grid(row=5, columnspan=2, pady=10)

        # Treeview to display members
        self.members_tree = ttk.Treeview(self.member_tab, columns=("ID", "Name", "Email", "Phone"), show="headings")
        self.members_tree.heading("ID", text="ID")
        self.members_tree.heading("Name", text="Name")
        self.members_tree.heading("Email", text="Email")
        self.members_tree.heading("Phone", text="Phone")
        self.members_tree.grid(row=6, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

        # Ensure the treeview expands
        self.member_tab.grid_rowconfigure(6, weight=1)
        self.member_tab.grid_columnconfigure(1, weight=1)

        self.refresh_members_list()

    def refresh_members_list(self):
        # Clear the treeview first
        for row in self.members_tree.get_children():
            self.members_tree.delete(row)

        # Fetch all members from the database
        with create_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Members")
            members = cursor.fetchall()

        # Insert members into the treeview
        for member in members:
            self.members_tree.insert("", "end", values=member)

    def add_member(self):
        name = self.member_name_entry.get()
        email = self.member_email_entry.get()
        phone = self.member_phone_entry.get()

        if not name or not email:
            messagebox.showerror("Error", "Name and Email are required.")
            return

        if not is_valid_email(email):
            messagebox.showerror("Error", "Invalid email format.")
            return

        with create_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO Members (name, email, phone, membership_date) VALUES (?, ?, ?, ?)",
                           (name, email, phone, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            conn.commit()

        self.refresh_members_list()
        messagebox.showinfo("Success", "Member added successfully!")
        self.clear_member_fields()

    def clear_member_fields(self):
        self.member_name_entry.delete(0, tk.END)
        self.member_email_entry.delete(0, tk.END)
        self.member_phone_entry.delete(0, tk.END)

    def delete_member(self):
        member_id = self.delete_member_id_entry.get()
        if not member_id.isdigit():
            messagebox.showerror("Error", "Member ID must be a number.")
            return

        with create_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Members WHERE member_id = ?", (int(member_id),))
            conn.commit()

        self.refresh_members_list()
        messagebox.showinfo("Success", "Member deleted successfully!")
        self.delete_member_id_entry.delete(0, tk.END)

    def create_transaction_widgets(self):
        # Transaction management UI code here
        ttk.Label(self.transaction_tab, text="Book ID:").grid(row=0, column=0, sticky='e', padx=5, pady=5)
        self.transaction_book_id_entry = ttk.Entry(self.transaction_tab)
        self.transaction_book_id_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.transaction_tab, text="Member ID:").grid(row=1, column=0, sticky='e', padx=5, pady=5)
        self.transaction_member_id_entry = ttk.Entry(self.transaction_tab)
        self.transaction_member_id_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Button(self.transaction_tab, text="Borrow Book", command=self.borrow_book).grid(row=2, columnspan=2, pady=10)

        # Entry for Transaction ID to return
        ttk.Label(self.transaction_tab, text="Transaction ID to Return:").grid(row=3, column=0, sticky='e', padx=5, pady=5)
        self.return_transaction_id_entry = ttk.Entry(self.transaction_tab)
        self.return_transaction_id_entry.grid(row=3, column=1, padx=5, pady=5)

        ttk.Button(self.transaction_tab, text="Return Book", command=self.return_book).grid(row=4, columnspan=2, pady=10)

        # Treeview to display transactions
        self.transactions_tree = ttk.Treeview(self.transaction_tab, columns=("ID", "Book ID", "Member ID", "Borrow Date", "Return Date"), show="headings")
        self.transactions_tree.heading("ID", text="ID")
        self.transactions_tree.heading("Book ID", text="Book ID")
        self.transactions_tree.heading("Member ID", text="Member ID")
        self.transactions_tree.heading("Borrow Date", text="Borrow Date")
        self.transactions_tree.heading("Return Date", text="Return Date")
        self.transactions_tree.grid(row=5, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

        # Ensure the treeview expands
        self.transaction_tab.grid_rowconfigure(5, weight=1)
        self.transaction_tab.grid_columnconfigure(1, weight=1)

        self.refresh_transactions_list()

    def refresh_transactions_list(self):
        # Clear the treeview first
        for row in self.transactions_tree.get_children():
            self.transactions_tree.delete(row)

        # Fetch all transactions from the database
        with create_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Transactions")
            transactions = cursor.fetchall()

        # Insert transactions into the treeview
        for transaction in transactions:
            self.transactions_tree.insert("", "end", values=transaction)

    def borrow_book(self):
        book_id = self.transaction_book_id_entry.get()
        member_id = self.transaction_member_id_entry.get()

        if not book_id.isdigit() or not member_id.isdigit():
            messagebox.showerror("Error", "Book ID and Member ID must be numbers.")
            return

        with create_connection() as conn:
            cursor = conn.cursor()
            # Insert the transaction into the database
            cursor.execute("INSERT INTO Transactions (book_id, member_id, borrow_date) VALUES (?, ?, ?)",
                           (int(book_id), int(member_id), datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            cursor.execute("UPDATE Books SET available_copies = available_copies - 1 WHERE book_id = ?", (int(book_id),))
            conn.commit()

        self.refresh_transactions_list()
        messagebox.showinfo("Success", "Book borrowed successfully!")
        self.clear_transaction_fields()

    def clear_transaction_fields(self):
        self.transaction_book_id_entry.delete(0, tk.END)
        self.transaction_member_id_entry.delete(0, tk.END)

    def return_book(self):
        transaction_id = self.return_transaction_id_entry.get()
        if not transaction_id.isdigit():
            messagebox.showerror("Error", "Transaction ID must be a number.")
            return

        with create_connection() as conn:
            cursor = conn.cursor()
            # Update the transaction with the return date
            cursor.execute("UPDATE Transactions SET return_date = ? WHERE transaction_id = ?",
                           (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), int(transaction_id)))
            cursor.execute("UPDATE Books SET available_copies = available_copies + 1 WHERE book_id = (SELECT book_id FROM Transactions WHERE transaction_id = ?)", (int(transaction_id),))
            conn.commit()

        self.refresh_transactions_list()
        messagebox.showinfo("Success", "Book returned successfully!")
        self.return_transaction_id_entry.delete(0, tk.END)

if __name__ == "__main__":
    app = LibraryApp()
    app.mainloop()
