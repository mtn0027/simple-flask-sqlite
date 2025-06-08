from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
DB_FILE = 'data.db'

def init_db():
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute('CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT)')
        conn.commit()

@app.route('/items', methods=['GET'])
def get_items():
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.execute('SELECT id, name FROM items')
        items = [{'id': row[0], 'name': row[1]} for row in cursor.fetchall()]
        return jsonify(items)

@app.route('/items', methods=['POST'])
def add_item():
    data = request.get_json()
    name = data.get('name')
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute('INSERT INTO items (name) VALUES (?)', (name,))
        conn.commit()
    return jsonify({'message': 'Item added'}), 201

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)
