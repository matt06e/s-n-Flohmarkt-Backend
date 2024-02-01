from flask import Flask, jsonify, request, send_file
import sqlite3
from flask_cors import CORS
from io import BytesIO
from datetime import datetime

app = Flask(__name__)
CORS(app)
app.config['DATABASE_FILE'] = 'index.db'
app.config['TABLE_NAME'] = 'products'
app.config['COMMENTS_TABLE'] = 'comments'

def create_product_dict(result):
    return {
        'id': result[0],
        'title': result[1],
        'price': result[2],
        'description': result[3],
        'location': result[4],
        'category': result[6],
        'payment_type': result[7],
        'get_type':result[8],
        'image_url': f"/product={result[0]}/image"
    }


def get_all_products():
    conn = sqlite3.connect(app.config['DATABASE_FILE'])
    cursor = conn.cursor()
    query = f"SELECT * FROM {app.config['TABLE_NAME']}"
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return [create_product_dict(result) for result in results]

def get_item_by_id(id):
    conn = sqlite3.connect(app.config['DATABASE_FILE'])
    cursor = conn.cursor()
    query = f"SELECT * FROM {app.config['TABLE_NAME']} WHERE id = ?"
    cursor.execute(query, (id,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    print(result) 
    return create_product_dict(result) if result else None

def get_image_by_id(id):
    conn = sqlite3.connect(app.config['DATABASE_FILE'])
    cursor = conn.cursor()
    query = f"SELECT image_data FROM {app.config['TABLE_NAME']} WHERE id = ?"
    cursor.execute(query, (id,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result[0] if result else None

def insert_data(title, price, description, location, image_data, get_type, category, payment_type):
    with sqlite3.connect(app.config['DATABASE_FILE']) as connection:
        cursor = connection.cursor()
        cursor.execute('''
            INSERT INTO products (title, price, description, location, image_data, type, category, payment_type)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (title, price, description, location, image_data, get_type, category, payment_type))
        connection.commit()

def get_comments_by_item_id(item_id):
    conn = sqlite3.connect(app.config['DATABASE_FILE'])
    cursor = conn.cursor()
    query = f"SELECT * FROM {app.config['COMMENTS_TABLE']} WHERE item_id = ?"
    cursor.execute(query, (item_id,))
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results

def add_comment(item_id, acount_id, comment):
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with sqlite3.connect(app.config['DATABASE_FILE']) as connection:
        cursor = connection.cursor()
        cursor.execute('''
            INSERT INTO comments (item_id, acount_id, comment, date)
            VALUES (?, ?, ?, ?)
        ''', (item_id, acount_id, comment, date))
        connection.commit()

@app.route('/comment=<int:item_id>', methods=['GET'])
def get_comments(item_id):
    comments = get_comments_by_item_id(item_id)
    return jsonify(comments)

@app.route('/comments', methods=['POST'])
def post_comment():
    data = request.get_json()
    item_id = data.get('item_id')
    acount_id = data.get('acount_id')
    comment_text = data.get('comment')

    if not item_id or not acount_id or not comment_text:
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        add_comment(item_id, acount_id, comment_text)
        return jsonify({'success': 'Comment added successfully'}), 201
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500

@app.route('/search=<string:search_query>', methods=['GET'])
def search_products(search_query):
    conn = sqlite3.connect(app.config['DATABASE_FILE'])
    cursor = conn.cursor()
    query = """
    SELECT * FROM products 
    WHERE title LIKE ? OR description LIKE ?;
    """
    search_pattern = f"%{search_query}%"
    cursor.execute(query, (search_pattern, search_pattern))
    results = cursor.fetchall()
    conn.close()
    products = [create_product_dict(result) for result in results]
    return jsonify(products)

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

@app.route('/ListItem', methods=['POST'])
def list_item():
    if request.method == 'POST':
        title = request.form.get('title')
        price = request.form.get('price')
        description = request.form.get('description')
        location = request.form.get('location')
        image_file = request.files.get('image')
        image_data = image_file.read()
        get_type = request.form.get('get_type')
        category = request.form.get('category')
        payment_type = request.form.get('payment_type')

        if not title or not price or not description or not location or not image_file:
            return jsonify({'error': 'Missing required fields'}), 400
        try:
            insert_data(title, price, description, location, image_data, get_type, category, payment_type)

            return jsonify({'success': 'Item listed successfully'}), 201
        except sqlite3.Error as e:
            return jsonify({'error': str(e)}), 500

@app.route('/product=<int:id>/image', methods=['GET'])
def get_product_image(id):
    image_data = get_image_by_id(id)
    if image_data:
        return send_file(BytesIO(image_data), mimetype='image/jpeg')
    else:
        return jsonify({'error': f'Image for Product with ID {id} not found.'}), 404

if __name__ == '__main__':
    app.run(debug=True)