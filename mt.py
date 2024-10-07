import csv
import sqlite3
import subprocess

# Database and table configuration
DB_NAME = 'example.db'
TABLE_NAME = 'commands'
SAMPLE_IN_PARAM = 'sample_input'
SAMPLE_OUT_PARAM = 'SELECT * FROM commands'
CSV_FILE_NAME = 'pipelines.csv'


# Create SQLite database and table
def create_database():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
            id INTEGER PRIMARY KEY,
            in_param TEXT,
            out_param TEXT
        )
    ''')
    # Insert a sample row
    cursor.execute(f"INSERT INTO {TABLE_NAME} (in_param, out_param) VALUES (?, ?)",
                   (SAMPLE_IN_PARAM, SAMPLE_OUT_PARAM))
    conn.commit()
    conn.close()


# Function to execute bash command and save output to SQLite
def execute_command(func, in_param, out_param):
    # Execute the bash command with parameters from IN
    result = subprocess.run(func.split() + [in_param], capture_output=True, text=True)

    # Connect to SQLite and save the output using the query from OUT
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Assume OUT is a SQL query to insert the result into the database
    cursor.execute(out_param, (result.stdout,))

    conn.commit()
    conn.close()


# Read from CSV and execute commands
def process_csv(file_name):
    with open(file_name, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            func = row['FUNC']
            in_param = row['IN']
            out_param = row['OUT']
            execute_command(func, in_param, out_param)


# Create the database and CSV file for demonstration
create_database()

# Sample CSV creation for testing purposes
with open(CSV_FILE_NAME, mode='w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=['FUNC', 'IN', 'OUT'])
    writer.writeheader()
    writer.writerow({'FUNC': 'echo', 'IN': 'Hello World!', 'OUT': f"INSERT INTO {TABLE_NAME} (in_param) VALUES (?)"})

# Process the CSV file
process_csv(CSV_FILE_NAME)
