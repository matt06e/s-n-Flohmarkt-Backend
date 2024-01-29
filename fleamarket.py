from flask import Flask, jsonify, request, send_file
import sqlite3
from flask_cors import CORS
from io import BytesIO

app = Flask(__name__)
CORS(app)
app.config['DATABASE_FILE'] = 'index.db'
app.config['TABLE_NAME'] = 'products'

# Routes
@app.route('/search=<string:search_query>', methods=['GET'])
def search_products(search_query):
    conn = sqlite3.connect(app.config['DATABASE_FILE'])
    cursor = conn.cursor()

    # Execute the SQL query with a parameterized statement to avoid SQL injection
    query = """
    SELECT * FROM products 
    WHERE title LIKE ? OR description LIKE ?;
    """

    # Use '%' to match any sequence of characters before and after the search_query
    search_pattern = f"%{search_query}%"
    
    cursor.execute(query, (search_pattern, search_pattern))

    # Fetch all the rows from the result set
    results = cursor.fetchall()

    # Close the database connection
    conn.close()

    # Convert the results to a list of dictionaries
    products = []
    for result in results:
        product_dict = {
            'id': result[0],
            'title': result[1],
            'price': result[2],
            'description': result[3],
            'location': result[4],
            'image_url': f"/product={result[0]}/image"  # Include image URL
        }
        products.append(product_dict)

    return jsonify(products)

# Get all products
@app.route('/products', methods=['GET'])
def get_all_items():
    products = get_all_products()
    return jsonify(products)

# Get product by ID
@app.route('/product=<int:id>', methods=['GET'])
def get_product(id):
    product = get_item_by_id(id)
    if product:
        return jsonify(product)
    else:
        return jsonify({'error': f'Product with ID {id} not found.'}), 404

# Get product image by ID
@app.route('/product=<int:id>/image', methods=['GET'])
def get_product_image(id):
    image_data = get_image_by_id(id)
    if image_data:
        return send_file(BytesIO(image_data), mimetype='image/jpeg')
    else:
        return jsonify({'error': f'Image for Product with ID {id} not found.'}), 404

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
            'location': result[4],
            'image_url': f"/product={result[0]}/image"  # Include image URL
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
            'location': result[4],
            'image_url': f"/product={result[0]}/image"  # Include image URL
        }
        return product_dict
    else:
        return None

# Function to get image by ID
def get_image_by_id(id):
    conn = sqlite3.connect(app.config['DATABASE_FILE'])
    cursor = conn.cursor()
    query = f"SELECT image_data FROM {app.config['TABLE_NAME']} WHERE id = ?"
    cursor.execute(query, (id,))

    result = cursor.fetchone()

    cursor.close()
    conn.close()

    if result:
        return result[0]
    else:
        return None

# Add a new product
@app.route('/ListItem', methods=['POST'])
def list_item():
    if request.method == 'POST':
        data = request.form
        title = data['title']
        price = data['price']
        description = data['description']
        location = data['location']

        # Get image file from the request
        image_file = request.files['image']

        try:
            image_data = image_file.read()  # Read binary data of the image
            insert_data(title, price, description, location, image_data)
            return jsonify(data), 201
        except sqlite3.Error as e:
            return jsonify({'error': str(e)}), 500

# Function to insert data into the database
def insert_data(title, price, description, location, image_data):
    with sqlite3.connect(app.config['DATABASE_FILE']) as connection:
        cursor = connection.cursor()
        cursor.execute('''
            INSERT INTO products (title, price, description, location, image_data)
            VALUES (?, ?, ?, ?, ?)
        ''', (title, price, description, location, image_data))
        connection.commit()

# Run the application
if __name__ == '__main__':
    app.run(debug=True)
