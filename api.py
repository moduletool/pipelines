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

@app.route('/api/flow_data/<int:flow_id>', methods=['GET'])
def get_flow_data_for_flow(flow_id):
    conn = get_db_connection()
    flow_data = conn.execute('''
        SELECT fd.id, func.name as function_name, fd.value, fd.type
        FROM flow_data fd
        JOIN flow_function ff ON fd.flow_id = ff.id
        JOIN functions func ON ff.function_id = func.id
        WHERE ff.flow_id = ?
        ORDER BY ff.id ASC
    ''', (flow_id,)).fetchall()
    conn.close()
    return jsonify([dict(obj) for obj in flow_data])

@app.route('/api/flow/<int:flow_id>', methods=['GET'])
def get_flow(flow_id):
    conn = get_db_connection()
    flow = conn.execute('SELECT * FROM flows WHERE id = ?', (flow_id,)).fetchone()
    flow_function = conn.execute('''
        SELECT ff.id, f.name as function_name, 
               GROUP_CONCAT(CASE WHEN fd.value IS NOT NULL THEN fd.value ELSE '' END) as valuess,
               GROUP_CONCAT(CASE WHEN fd.type IS NOT NULL THEN fd.type ELSE '' END) as types
        FROM flow_function ff
        JOIN functions f ON ff.function_id = f.id
        LEFT JOIN flow_data fd ON ff.id = fd.flow_id
        WHERE ff.flow_id = ?
        GROUP BY ff.id
        ORDER BY ff.id ASC
    ''', (flow_id,)).fetchall()
    conn.close()
    
    return jsonify({
        'id': flow['id'],
        'name': flow['name'],
        'flow_function': [dict(cmd) for cmd in flow_function]
    })

@app.route('/api/all_flow_data', methods=['GET'])
def get_all_flow_data():
    conn = get_db_connection()
    flow_data = conn.execute('''
        SELECT fd.id, f.name as flow_name, func.name as function_name, fd.value, fd.type
        FROM flow_data fd
        JOIN flow_function ff ON fd.flow_id = ff.id
        JOIN flows f ON ff.flow_id = f.id
        JOIN functions func ON ff.function_id = func.id
        ORDER BY f.id DESC, ff.id ASC
    ''').fetchall()
    conn.close()
    return jsonify([dict(obj) for obj in flow_data])


@app.route('/api/run_flow', methods=['POST'])
def run_flow():
    try:
        flow_data = request.json
        nodes = flow_data['nodes']
        edges = flow_data['edges']
        flow_name = flow_data['flowName']

        # Save the flow
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO flows (name) VALUES (?)', (flow_name,))
        flow_id = cursor.lastrowid

        # Save flow_function and flow objects
        for node in nodes:
            function = conn.execute('SELECT id FROM functions WHERE name = ?', (node['data']['label'],)).fetchone()
            if function:
                cursor.execute('INSERT INTO flow_function (flow_id, function_id) VALUES (?, ?)',
                               (flow_id, function['id']))
                flow_id = cursor.lastrowid
                type = 'input'
                for value in node['data']['inputs']:
                    cursor.execute('INSERT INTO flow_data (flow_id, value, type) VALUES (?, ?, ?)',
                                   (flow_id, value, type))

        conn.commit()

        # Process the flow
        result = process_flow(nodes, edges)
        print(result)

        # Save output as flow objects
        for node_id, output in result.items():
            print(node_id, output)
            # flow = conn.execute('SELECT id FROM flow_function WHERE flow_id = ? AND id = ?', (flow_id, node_id)).fetchone()
            # if flow:
            type = 'output'
            value=str(output)
            cursor.execute('INSERT INTO flow_data (flow_id, value, type) VALUES (?, ?, ?)',
                           # (flow['id'], value, type))
                           (flow_id, value, type))
                # cursor.execute('UPDATE flow_data SET output = ? WHERE flow_id = ?',
                #                (str(output), flow['id']))
        conn.commit()
        conn.close()

        return jsonify({
            "message": "Flow executed and saved successfully",
            "result": result,
            "flow_id": flow_id
        })
    except Exception as e:
        # If an error occurs, rollback the transaction and return an error message
        if 'conn' in locals():
            conn.rollback()
            conn.close()
        return jsonify({"error": str(e)}), 500



@app.route('/api/flow/<int:flow_id>', methods=['DELETE'])
def delete_flow(flow_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Usuń powiązane flow_data
        cursor.execute('DELETE FROM flow_data WHERE flow_id IN (SELECT id FROM flow_function WHERE flow_id = ?)', (flow_id,))

        # Usuń powiązane flow_function
        cursor.execute('DELETE FROM flow_function WHERE flow_id = ?', (flow_id,))

        # Usuń flow
        cursor.execute('DELETE FROM flows WHERE id = ?', (flow_id,))

        conn.commit()
        return jsonify({"message": "Flow deleted successfully"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

def process_flow(nodes, edges):
    result = {}
    for node in nodes:
        function_name = node['data']['label']
        inputs = node['data']['inputs']
        try:
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
            else:
                result[node['id']] = f"Unknown function: {function_name}"
        except Exception as e:
            result[node['id']] = f"Error processing node: {str(e)}"
    return result

if __name__ == '__main__':
    app.run(debug=True)