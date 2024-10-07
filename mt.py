import csv
import sqlite3
import subprocess

# Database and table configuration
DB_NAME = 'db.sqlite'

FUNC_TABLE = 'functions'
# CMD_NAME = f'SELECT name FROM {FUNC_TABLE} LIMIT 1'
CMD_FUNC_NAME = 'echo'

CMD_TABLE = 'commands'
CMD_FUNC = f'SELECT name FROM {FUNC_TABLE} LIMIT 1'
CMD_IN = f'SELECT value FROM {CMD_TABLE} LIMIT 1'
CMD_OUT = f"INSERT INTO {CMD_TABLE} (output) VALUES (?)"

DATA_TABLE = 'objects'
DATA_IN = f"SELECT input FROM {DATA_TABLE} WHERE id = 1"
DATA_OUT = f"UPDATE {DATA_TABLE} SET output=(?) WHERE id = 1"
# DATA_OUT = "INSERT INTO objects (output) VALUES (?)"

CSV_FILE_NAME = 'pipelines.csv'


# UPDATE my_table SET name = 'example', value = 'new_value' WHERE id = 1;


# Create SQLite database and table
def create_database():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(f'''
           CREATE TABLE IF NOT EXISTS {FUNC_TABLE} (
               id INTEGER PRIMARY KEY,
               name TEXT
           )
       ''')
    # Insert a sample row
    cursor.execute(f"INSERT INTO {FUNC_TABLE} (name) VALUES (?)", (CMD_FUNC_NAME,))

    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {CMD_TABLE} (
            id INTEGER PRIMARY KEY,
            func TEXT,
            input TEXT,
            output TEXT
        )
    ''')
    # Insert a sample row
    cursor.execute(f"INSERT INTO {CMD_TABLE} (func, input, output) VALUES (?, ?, ?)", (CMD_FUNC, DATA_IN, DATA_OUT))

    cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS {DATA_TABLE} (
                id INTEGER PRIMARY KEY,
                func TEXT,
                input TEXT,
                output TEXT
            )
        ''')
    # Insert a sample row
    cursor.execute(f"INSERT INTO {DATA_TABLE} (func, input, output) VALUES (?, ?, ?)", ('echo', 'test1', ''))
    conn.commit()
    conn.close()


import subprocess


def run(command="echo 'Hello, World!'"):
    # Define the bash command as a string or as a list of arguments
    try:
        # Run the command
        # If you're using a string and want to use shell features like globbing or pipes, use shell=True
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)

        # Print the command's output
        print("Command Output:", result.stdout)

        # If there's any error output
        if result.stderr:
            print("Command Error Output:", result.stderr)

    except subprocess.CalledProcessError as e:
        print(f"An error occurred while executing the command: {e}")


def run2(command=["echo", "Hello, World!"]):  # Define the command and arguments as a list

    try:
        # Run the command
        result = subprocess.run(command, check=True, capture_output=True, text=True)

        # Print the command's output
        print("Command Output:", result.stdout)

    except subprocess.CalledProcessError as e:
        print(f"An error occurred while executing the command: {e}")


# Function to execute bash command and save GET_OUT_SQL to SQLite
def execute_command(GET_CMD_SQL, GET_IN_SQL, GET_OUT_SQL):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(GET_CMD_SQL)
    result = cursor.fetchone()  # Fetch the first result

    if result:
        func = result[0]  # Assuming the value we need is in the first column
        print(func)

        # Execute the SQL query from IN parameter to get the GET_IN_SQL value
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        cursor.execute(GET_IN_SQL)
        result = cursor.fetchone()  # Fetch the first result

        if result:
            input_value = result[0]  # Assuming the value we need is in the first column

            cmds = []
            # cmd.append('pwd')  # Add the command to the list
            cmds.append(func)  # Add the command to the list
            print(func)

            # cmd.append('./'+func)  # Add the command to the list
            # cmd.append('"' + input_value + '"')  # Add the command to the list
            print(input_value)
            if input_value != None:
                cmds.append(input_value)  # Add the command to the list
            # join the command elements into a single string
            cmd = " ".join(cmds)  # Join the command elements into a single string
            print(cmd)
            # print()
            # Execute the bash command with parameters from IN
            # command_result = subprocess.run(cmd, capture_GET_OUT_SQL=True, text=True)
            # Define the bash command as a string or as a list of arguments
            try:

                # Run the command
                # If you're using a string and want to use shell features like globbing or pipes, use shell=True
                result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)

                # Print the command's output
                print("output:", result)
                print("output:", GET_OUT_SQL)
                print("Output:", result.stdout)
                # Save the output using the query from OUT
                cursor.execute(GET_OUT_SQL, (result.stdout,))

                # If there's any error output
                if result.stderr:
                    print("Command Error Output:", result.stderr)

            except subprocess.CalledProcessError as e:
                print(f"An error occurred while executing the command: {e}")

        else:
            print("No input INPUT")

    else:
        print("No input FUNCTION")

    print(result)

    conn.commit()
    conn.close()


# Read from CSV and execute commands
def process_csv(file_name):
    with open(file_name, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            func = row['FUNC']
            input = row['IN']
            output = row['OUT']
            execute_command(func, input, output)


# Read from CSV and execute commands
def run_sql(GET_CMD_SQL):
    # CMD_FUNC = f'SELECT name FROM {FUNC_TABLE} LIMIT 1'
    # CMD_IN = f'SELECT value FROM {CMD_TABLE} LIMIT 1'
    # CMD_OUT = f"INSERT INTO {CMD_TABLE} (output) VALUES (?)"

    # Execute the SQL query from IN parameter to get the GET_IN_SQL value
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(GET_CMD_SQL)
    outs = cursor.fetchone()  # Fetch the first result
    if outs:
        print(outs[0],
              outs[1],
              outs[2])
        execute_command(outs[0],
                        outs[1],
                        outs[2])
    print(outs)

    conn.commit()
    conn.close()


# Sample CSV creation for testing purposes
def create_csv_file(CSV_FILE_NAME):
    with open(CSV_FILE_NAME, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['FUNC', 'IN', 'OUT'])
        writer.writeheader()
        writer.writerow({'FUNC': 'echo', 'IN': CMD_IN, 'OUT': CMD_OUT})


# output = create_database()
# Process the CSV file
# create_csv_file(CSV_FILE_NAME)
# GET_CMD_SQL = f"# SELECT func, input, output FROM {CMD_TABLE} WHERE id = 1"
# GET_CMD_SQL = f"SELECT func, input, output FROM {CMD_TABLE} WHERE id = 2"
GET_CMD_SQL = f"SELECT func, input, output FROM {CMD_TABLE} WHERE id = 3"
run_sql(GET_CMD_SQL)
# run()
# output = ''
# output = execute_command('echo', CMD_IN, CMD_OUT)
# execute_command('echo', 'input', output)

# command_result = subprocess.run('python echo.py test', capture_output=True, text=True)
# command_result = subprocess.run('./echo1.sh', capture_output=True, text=True)
# command_result = subprocess.run(['./echo.py','222'], capture_output=True, text=True)
# output = command_result.stdout
# print(output)
