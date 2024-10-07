import sqlite3

def setup_database():
    conn = sqlite3.connect('flow_diagram.db')
    cursor = conn.cursor()

    # Create tables
    cursor.executescript('''
    CREATE TABLE functions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        description TEXT,
        name TEXT NOT NULL,
        type TEXT NOT NULL
    );

    CREATE TABLE flows (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    );

    CREATE TABLE objects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        input TEXT,
        output TEXT
    );

    CREATE TABLE commands (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        flow_id INTEGER,
        command_id INTEGER,
        function_id INTEGER,
        object_id INTEGER,
        FOREIGN KEY (flow_id) REFERENCES flows(id),
        FOREIGN KEY (function_id) REFERENCES functions(id),
        FOREIGN KEY (object_id) REFERENCES objects(id)
    );
    ''')

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