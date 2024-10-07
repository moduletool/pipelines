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

@app.route('/api/flows', methods=['GET'])
def get_flows():
    conn = get_db_connection()
    flows = conn.execute('SELECT * FROM flows').fetchall()
    conn.close()
    return jsonify([dict(flow) for flow in flows])

@app.route('/api/command_objects/<int:flow_id>', methods=['GET'])
def get_command_objects_for_flow(flow_id):
    conn = get_db_connection()
    command_objects = conn.execute('''
        SELECT co.id, func.name as function_name, co.input, co.output
        FROM command_objects co
        JOIN commands c ON co.command_id = c.id
        JOIN functions func ON c.function_id = func.id
        WHERE c.flow_id = ?
        ORDER BY c.id ASC
    ''', (flow_id,)).fetchall()
    conn.close()
    return jsonify([dict(obj) for obj in command_objects])

@app.route('/api/flow/<int:flow_id>', methods=['GET'])
def get_flow(flow_id):
    conn = get_db_connection()
    flow = conn.execute('SELECT * FROM flows WHERE id = ?', (flow_id,)).fetchone()
    commands = conn.execute('''
        SELECT c.id, f.name as function_name, 
               GROUP_CONCAT(CASE WHEN co.input IS NOT NULL THEN co.input ELSE '' END) as inputs,
               GROUP_CONCAT(CASE WHEN co.output IS NOT NULL THEN co.output ELSE '' END) as outputs
        FROM commands c
        JOIN functions f ON c.function_id = f.id
        LEFT JOIN command_objects co ON c.id = co.command_id
        WHERE c.flow_id = ?
        GROUP BY c.id
        ORDER BY c.id ASC
    ''', (flow_id,)).fetchall()
    conn.close()
    
    return jsonify({
        'id': flow['id'],
        'name': flow['name'],
        'commands': [dict(cmd) for cmd in commands]
    })

@app.route('/api/all_command_objects', methods=['GET'])
def get_all_command_objects():
    conn = get_db_connection()
    command_objects = conn.execute('''
        SELECT co.id, f.name as flow_name, func.name as function_name, co.input, co.output
        FROM command_objects co
        JOIN commands c ON co.command_id = c.id
        JOIN flows f ON c.flow_id = f.id
        JOIN functions func ON c.function_id = func.id
        ORDER BY f.id DESC, c.id ASC
    ''').fetchall()
    conn.close()
    return jsonify([dict(obj) for obj in command_objects])

@app.route('/api/run_flow', methods=['POST'])
def run_flow():
    flow_data = request.json
    nodes = flow_data['nodes']
    edges = flow_data['edges']
    flow_name = flow_data['flowName']

    # Save the flow
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO flows (name) VALUES (?)', (flow_name,))
    flow_id = cursor.lastrowid

    # Save commands and command objects
    for node in nodes:
        function = conn.execute('SELECT id FROM functions WHERE name = ?', (node['data']['label'],)).fetchone()
        if function:
            cursor.execute('INSERT INTO commands (flow_id, function_id) VALUES (?, ?)', 
                           (flow_id, function['id']))
            command_id = cursor.lastrowid
            for input_value in node['data']['inputs']:
                cursor.execute('INSERT INTO command_objects (command_id, input) VALUES (?, ?)',
                               (command_id, input_value))

    conn.commit()

    # Process the flow
    result = process_flow(nodes, edges)

    # Save output as command objects
    for node_id, output in result.items():
        command = conn.execute('SELECT id FROM commands WHERE flow_id = ? AND id = ?', (flow_id, node_id)).fetchone()
        if command:
            cursor.execute('UPDATE command_objects SET output = ? WHERE command_id = ?', 
                           (str(output), command['id']))
    conn.commit()
    conn.close()

    @app.route('/api/flow/<int:flow_id>', methods=['DELETE'])
    def delete_flow(flow_id):
        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            # Usuń powiązane command_objects
            cursor.execute(
                'DELETE FROM command_objects WHERE command_id IN (SELECT id FROM commands WHERE flow_id = ?)',
                (flow_id,))

            # Usuń powiązane commands
            cursor.execute('DELETE FROM commands WHERE flow_id = ?', (flow_id,))

            # Usuń flow
            cursor.execute('DELETE FROM flows WHERE id = ?', (flow_id,))

            conn.commit()
            return jsonify({"message": "Flow deleted successfully"}), 200
        except Exception as e:
            conn.rollback()
            return jsonify({"error": str(e)}), 500
        finally:
            conn.close()

    return jsonify({"message": "Flow executed and saved successfully", "result": result})

def process_flow(nodes, edges):
    result = {}
    for node in nodes:
        function_name = node['data']['label']
        inputs = node['data']['inputs']
        if function_name == 'add':
            result[node['id']] = add(float(inputs[0]), float(inputs[1]))
        elif function_name == 'subtract':
            result[node['id']] = subtract(float(inputs[0]), float(inputs[1]))
        elif function_name == 'multiply':
            result[node['id']] = multiply(float(inputs[0]), float(inputs[1]))
        elif function_name == 'divide':
            result[node['id']] = divide(float(inputs[0]), float(inputs[1]))
        elif function_name == 'evaluate_expression':
            result[node['id']] = evaluate_expression(inputs[0])
    return result

if __name__ == '__main__':
    app.run(debug=True)