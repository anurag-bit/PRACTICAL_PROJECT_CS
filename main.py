import mysql.connector

# Connect to the database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="ROOT@sql"
)

# Create a cursor to execute queries
cursor = db.cursor()

# Check if the database exists
database_name = "library"
check_database_query = f"SHOW DATABASES LIKE '{database_name}'"
cursor.execute(check_database_query)
print("databse exists already!")

# If the database does not exist, create it
if not cursor.fetchone():
    create_database_query = f"CREATE DATABASE {database_name}"
    cursor.execute(create_database_query)
    print(f"The database '{database_name}' was created.")

# Select the database
use_database_query = f"USE {database_name}"
cursor.execute(use_database_query)

# Create the books table if it does not exist
create_books_table_query = """
CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(255) NOT NULL,
    author VARCHAR(255) NOT NULL,
    year_published INTEGER NOT NULL,
    isbn VARCHAR(255) NOT NULL,
    genre VARCHAR(255) NOT NULL,
    availability BOOLEAN NOT NULL DEFAULT TRUE
)
"""
cursor.execute(create_books_table_query)

# Create the patrons table if it does not exist
create_patrons_table_query = ("\n"
                              "CREATE TABLE IF NOT EXISTS patrons (\n"
                              "    id INTEGER PRIMARY KEY AUTO_INCREMENT,\n"
                              "    first_name VARCHAR(255) NOT NULL,\n"
                              "    last_name VARCHAR(255) NOT NULL,\n"
                              "    email VARCHAR(255) NOT NULL,\n"
                              "    phone VARCHAR(255) NOT NULL\n"
                              ")\n")
cursor.execute(create_patrons_table_query)

# Create the transactions table if it does not exist
create_transactions_table_query = """
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    book_id INTEGER NOT NULL,
    patron_id INTEGER NOT NULL,
    check_out_date DATE NOT NULL,
    due_date DATE NOT NULL,
    return_date DATE,
    FOREIGN KEY (book_id) REFERENCES books(id),
    FOREIGN KEY (patron_id) REFERENCES patrons(id)
)
"""
cursor.execute(create_transactions_table_query)

# Commit the changes to the database
db.commit()

# Display a menu to the user
while True:
    print("--- Menu ---")
    print("1. Issue a book")
    print("2. Query books")
    print("3. View borrowers details")
    print("4. Add a transaction")
    print("5. Exit")
    print()

    # Read the user's choice
    choice = input("Enter your choice: ")

    # Take action based on the choice
    if choice == "1":
        # Issue a book
        # Read the input from the user
        book_id = input("Enter the book ID: ")
        patron_id = input("Enter the patron ID: ")
        check_out_date = input("Enter the check-out date (YYYY-MM-DD): ")
        due_date = input("Enter the due date (YYYY-MM-DD): ")
        first_name = input("Enter First Name: ")
        last_name = input("ENTER YOUR LAST NAME: ")
        email = input("ENTER EMAIL:  ")
        phone = input("ENTER YOUR PHONE NUMBER: ")


        # Construct the INSERT INTO query
        def issue_book(cursor, book_id, patron_id, check_out_date, due_date, first_name, last_name, email, phone):
            # Check if the patron exists in the database
            select_query = f"SELECT * FROM patrons WHERE id = {patron_id}"
            cursor.execute(select_query)
            if cursor.fetchone():
                # The patron already exists in the database, so update the transaction table
                insert_query = """
                INSERT INTO transactions (book_id, patron_id, check_out_date, due_date)
                VALUES (%s, %s, %s, %s)
                """
                cursor.execute(insert_query, (book_id, patron_id, check_out_date, due_date))
            else:
                # The patron does not exist in the database, so insert them into the patrons table and update the
                # 1transaction table
                insert_patron_query = """
                INSERT INTO patrons (id, first_name, last_name, email, phone)
                VALUES (%s, %s, %s, %s, %s)
                """
                cursor.execute(insert_patron_query, (patron_id, first_name, last_name, email, phone))
                insert_query = """
                INSERT INTO transactions (book_id, patron_id, check_out_date, due_date)
                VALUES (%s, %s, %s, %s)
                """
                cursor.execute(insert_query, (book_id, patron_id, check_out_date, due_date))

            issue_book(book_id, patron_id, check_out_date, due_date, first_name, last_name, email, phone)


        db.commit()

        pass
    elif choice == "2":
        # Query books
        select_query = """
        SELECT b.title, p.first_name, p.last_name, t.check_out_date, t.due_date
        FROM transactions t
        INNER JOIN books b ON b.id = t.book_id
        INNER JOIN patrons p ON p.id = t.patron_id
        """

        # Execute the query
        cursor.execute(select_query)

        # Fetch the results
        results = cursor.fetchall()


        # Print the results
        def reults():

            for result in results:
                title, first_name, last_name, check_out_date, due_date = result
                print(f"Book: {title}")
                print(f"Borrower: {first_name} {last_name}")
                print(f"Check-out date: {check_out_date}")
                print(f"Due date: {due_date}")
                print()


        pass
    elif choice == "3":
        # View borrowers details
        def view_borrowers(cursor):
            # Construct the SELECT query
            select_query = """
            SELECT * FROM patrons
            """

            # Execute the query
            cursor.execute(select_query)

            # Fetch the results
            results = cursor.fetchall()

            # Print the results
            for result in results:
                id, first_name, last_name, email, phone = result
                print(f"ID: {id}")
                print(f"Name: {first_name} {last_name}")
                print(f"Email: {email}")
                print(f"Phone: {phone}")
                print()
        pass
    elif choice == "4":
        # Add a transaction
        def add_transaction(cursor, book_id, patron_id, check_out_date, due_date):
            # Construct the INSERT INTO query
            insert_query = """
            INSERT INTO transactions (book_id, patron_id, check_out_date, due_date)
            VALUES (%s, %s, %s, %s)
            """

            # Execute the query
            cursor.execute(insert_query, (book_id, patron_id, check_out_date, due_date))

            # Print a message to confirm the addition
            print("Transaction added successfully.")


        pass
    elif choice == "5":
        # Exit the program
        break
    else:
        # Invalid choice
        print("Invalid choice. Please try again.")
        print()
