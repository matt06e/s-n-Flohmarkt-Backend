from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)
app.config['DATABASE_FILE'] = 'index.db'
app.config['TABLE_NAME'] = 'products'


# Routes
@app.route('/product=<int:id>', methods=['GET'])
def get_product(id):
    product = get_item_by_id(id)
    if product:
        return jsonify({
            'id': product[0],
            'title': product[1],
            'price': product[2],
            'description': product[3]
        })
    else:
        return f'Product with ID {id} not found.', 404

# Function to get product by ID
def get_item_by_id(id):
    conn = sqlite3.connect(app.config['DATABASE_FILE'])
    cursor = conn.cursor()
    query = f"SELECT * FROM {app.config['TABLE_NAME']} WHERE id = ?"
    cursor.execute(query, (id,))

    result = cursor.fetchone()

    cursor.close()
    conn.close()

    return result


@app.route('/ListItem', methods=['POST'])
def list_item():
    if request.method == 'POST':
        data = request.get_json()
        if not all(key in data for key in ('title', 'price', 'description')):
            return jsonify({'error': 'Missing required fields'}), 400
        try:
            insert_data(data['title'], data['price'], data['description'])
            return jsonify(data), 201
        except sqlite3.Error as e:
            return jsonify({'error': str(e)}), 500

def insert_data(title, price, description):
    with sqlite3.connect(app.config['DATABASE_FILE']) as connection:
        cursor = connection.cursor()
        cursor.execute('''
            INSERT INTO products (title, price, description)
            VALUES (?, ?, ?)
        ''', (title, price, description))
        connection.commit()

if __name__ == '__main__':
    app.run(debug=True)
