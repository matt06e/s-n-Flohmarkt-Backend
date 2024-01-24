from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)
app.config['DATABASE_FILE'] = 'index.db'
app.config['TABLE_NAME'] = 'products'


# Routes
@app.route('/products', methods=['GET'])
def get_all_items():
    products = get_all_products()
    return jsonify(products)


@app.route('/product=<int:id>', methods=['GET'])
def get_product(id):
    product = get_item_by_id(id)
    if product:
        return jsonify(product)
    else:
        return jsonify({'error': f'Product with ID {id} not found.'}), 404


# Function to get all products
def get_all_products():
    conn = sqlite3.connect(app.config['DATABASE_FILE'])
    cursor = conn.cursor()
    query = f"SELECT * FROM {app.config['TABLE_NAME']}"
    cursor.execute(query)

    results = cursor.fetchall()

    cursor.close()
    conn.close()

    # Convert the results to a list of dictionaries
    products = []
    for result in results:
        product_dict = {
            'id': result[0],
            'title': result[1],
            'price': result[2],
            'description': result[3],
            'location': result[4]  # Added 'location' field
        }
        products.append(product_dict)

    return products


# Function to get product by ID
def get_item_by_id(id):
    conn = sqlite3.connect(app.config['DATABASE_FILE'])
    cursor = conn.cursor()
    query = f"SELECT * FROM {app.config['TABLE_NAME']} WHERE id = ?"
    cursor.execute(query, (id,))

    result = cursor.fetchone()

    cursor.close()
    conn.close()

    if result:
        product_dict = {
            'id': result[0],
            'title': result[1],
            'price': result[2],
            'description': result[3],
            'location': result[4]  # Added 'location' field
        }
        return product_dict
    else:
        return None


@app.route('/ListItem', methods=['POST'])
def list_item():
    if request.method == 'POST':
        data = request.get_json()
        if not all(key in data for key in ('title', 'price', 'description', 'location')):
            return jsonify({'error': 'Missing required fields'}), 400
        try:
            insert_data(data['title'], data['price'], data['description'], data['location'])
            return jsonify(data), 201
        except sqlite3.Error as e:
            return jsonify({'error': str(e)}), 500


def insert_data(title, price, description, location):
    with sqlite3.connect(app.config['DATABASE_FILE']) as connection:
        cursor = connection.cursor()
        cursor.execute('''
            INSERT INTO products (title, price, description, location)
            VALUES (?, ?, ?, ?)
        ''', (title, price, description, location))
        connection.commit()


if __name__ == '__main__':
    app.run(debug=True)
