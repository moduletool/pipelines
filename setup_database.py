import sqlite3
import os

def setup_database():
    db_name = 'flow_diagram.db'
    
    # Remove existing database if it exists
    if os.path.exists(db_name):
        os.remove(db_name)
        print(f"Existing database '{db_name}' removed.")

    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Read schema from file
    with open('schema.sql', 'r') as schema_file:
        schema_script = schema_file.read()

    # Create tables
    cursor.executescript(schema_script)

    # Insert sample functions
    sample_functions = [
        ('Echo input', 'echo', 'shell'),
        ('Evaluate expression', 'expr', 'python'),
        ('Add two numbers', 'add', 'python'),
        ('Subtract two numbers', 'subtract', 'python'),
        ('Multiply two numbers', 'multiply', 'python'),
        ('Divide two numbers', 'divide', 'python'),
    ]

    cursor.executemany('''
    INSERT INTO functions (description, name, type)
    VALUES (?, ?, ?)
    ''', sample_functions)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    setup_database()
    print("Database setup complete.")