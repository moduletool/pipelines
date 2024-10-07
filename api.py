from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
from calculator_functions import add, subtract, multiply, divide, evaluate_expression

app = Flask(__name__)
CORS(app)

def get_db_connection():
    conn = sqlite3.connect('flow_diagram.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/api/functions', methods=['GET'])
def get_functions():
    conn = get_db_connection()
    functions = conn.execute('SELECT * FROM functions').fetchall()
    conn.close()
    return jsonify([dict(func) for func in functions])

@app.route('/api/objects', methods=['GET'])
def get_objects():
    conn = get_db_connection()
    objects = conn.execute('SELECT * FROM objects').fetchall()
    conn.close()
    return jsonify([dict(obj) for obj in objects])

@app.route('/api/run_flow', methods=['POST'])
def run_flow():
    flow_data = request.json
    nodes = flow_data['nodes']
    edges = flow_data['edges']
    flow_name = flow_data['flowName']
    input_data = flow_data['inputData']

    # Save the flow
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO flows (name) VALUES (?)', (flow_name,))
    flow_id = cursor.lastrowid

    # Save commands (nodes and edges)
    for node in nodes:
        cursor.execute('INSERT INTO commands (flow_id, function_id) VALUES (?, ?)', 
                       (flow_id, node['data']['label']))

    conn.commit()

    # Process the flow
    result = process_flow(nodes, edges, input_data)

    # Save input and output as objects
    cursor.execute('INSERT INTO objects (input, output) VALUES (?, ?)', 
                   (input_data, result))
    conn.commit()
    conn.close()

    return jsonify({"message": "Flow executed and saved successfully", "result": result})

def process_flow(nodes, edges, input_data):
    # This is a simplified flow processing function
    # In a real scenario, you'd need to handle more complex flows
    result = input_data
    for node in nodes:
        function_name = node['data']['label']
        if function_name == 'add':
            result = add(float(result), 10)  # Just an example, add 10 to the result
        elif function_name == 'subtract':
            result = subtract(float(result), 5)  # Subtract 5 from the result
        elif function_name == 'multiply':
            result = multiply(float(result), 2)  # Multiply the result by 2
        elif function_name == 'divide':
            result = divide(float(result), 2)  # Divide the result by 2
        elif function_name == 'evaluate_expression':
            result = evaluate_expression(result)
    return str(result)

if __name__ == '__main__':
    app.run(debug=True)