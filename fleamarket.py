from flask import Flask, jsonify, request, send_file
import sqlite3
from flask_cors import CORS
from io import BytesIO
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Configuration
app.config['DATABASE_FILE'] = 'index.db'
app.config['TABLE_NAME'] = 'products'
app.config['COMMENTS_TABLE'] = 'comments'
app.config['ACCOUNT_TABLE'] = 'accounts'

# Helper functions
def create_product_dict(result):
    return {
        'id': result[0],
        'account_id': result[1],
        'title': result[2],
        'price': result[3],
        'description': result[4],
        'location': result[5],
        'category': result[7],
        'payment_type': result[8],
        'get_typ': result[9],
        'image_url': f"/product={result[0]}/image"
    }

def create_account_dict(result):
    return {
        'account_id': result[0],
        'name': result[1],
        'create_date': result[2],
        'location': result[3],
        'image_url': f"/product={result[0]}/image"
    }

def connect_to_database():
    return sqlite3.connect(app.config['DATABASE_FILE'])

def execute_query(query, params=None):
    with connect_to_database() as conn:
        cursor = conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        return cursor

# Database operations
def get_all_products():
    query = f"SELECT * FROM {app.config['TABLE_NAME']}"
    results = execute_query(query).fetchall()
    return [create_product_dict(result) for result in results]

def get_item_by_id(product_id):
    query = f"SELECT * FROM {app.config['TABLE_NAME']} WHERE id = ?"
    result = execute_query(query, (product_id,)).fetchone()
    return create_product_dict(result) if result else None

def get_image_by_id(product_id):
    query = f"SELECT image_data FROM {app.config['TABLE_NAME']} WHERE id = ?"
    result = execute_query(query, (product_id,)).fetchone()
    return result[0] if result else None

def insert_data(account_id, title, price, description, location, image_data, get_typ, category, payment_type):
    query = '''
        INSERT INTO products (account_id, title, price, description, location, image_data, get_typ, category, payment_type)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    '''
    params = (account_id, title, price, description, location, image_data, get_typ, category, payment_type)
    execute_query(query, params)

# Comments operations
def get_comments_by_item_id(item_id):
    query = f"SELECT * FROM {app.config['COMMENTS_TABLE']} WHERE item_id = ?"
    results = execute_query(query, (item_id,)).fetchall()
    return results

def add_comment(item_id, account_id, comment):
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    query = '''
        INSERT INTO comments (item_id, account_id, comment, date)
        VALUES (?, ?, ?, ?)
    '''
    params = (item_id, account_id, comment, date)
    execute_query(query, params)

# Routes
@app.route('/comment=<int:item_id>', methods=['GET'])
def get_comments(item_id):
    comments = get_comments_by_item_id(item_id)
    return jsonify(comments)

@app.route('/comments', methods=['POST'])
def post_comment():
    data = request.get_json()
    item_id, account_id, comment_text = data.get('item_id'), data.get('account_id'), data.get('comment')

    try:
        add_comment(item_id, account_id, comment_text)
        return jsonify({'success': 'Comment added successfully'}), 201
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500

@app.route('/search=<string:search_query>', methods=['GET'])
def search_products(search_query):
    query = """
        SELECT * FROM products 
        WHERE title LIKE ? OR description LIKE ?;
    """
    search_pattern = f"%{search_query}%"
    results = execute_query(query, (search_pattern, search_pattern)).fetchall()
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
        title, price, description, location, image_file = (
            request.form.get('title'),
            request.form.get('price'),
            request.form.get('description'),
            request.form.get('location'),
            request.files.get('image'),
        )
        image_data = image_file.read() if image_file else None
        get_typ, category, payment_type, account_id = (
            request.form.get('get_typ'),
            request.form.get('category'),
            request.form.get('payment_type'),
            request.form.get('account_id'),
        )

        try:
            insert_data(account_id, title, price, description, location, image_data, get_typ, category, payment_type)
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

@app.route('/account_items=<int:account_id>', methods=['GET'])
def get_items_by_account_id(account_id):
    query = f"SELECT * FROM {app.config['TABLE_NAME']} WHERE account_id = ?"
    results = execute_query(query, (account_id,)).fetchall()
    items = [create_product_dict(result) for result in results]
    return jsonify(items)

@app.route('/account=<int:account_id>')
def get_account_by_id(account_id):
    query = f"SELECT * FROM {app.config['ACCOUNT_TABLE']} WHERE account_id = ?"
    result = execute_query(query, (account_id,)).fetchone()
    return create_account_dict(result) if result else None

@app.route('/account=<int:account_id>/image', methods=['GET'])
def get_account_image(account_id):
    image_data = get_image_by_account_id(account_id)
    if image_data:
        return send_file(BytesIO(image_data), mimetype='image/jpeg')
    else:
        return jsonify({'error': f'Image for Account with ID {account_id} not found.'}), 404

def get_image_by_account_id(account_id):
    query = f"SELECT profile_picture FROM {app.config['ACCOUNT_TABLE']} WHERE account_id = ?"
    result = execute_query(query, (account_id,)).fetchone()
    return result[0] if result else None

def insert_account(name, location, profile_picture):
    query = '''
        INSERT INTO account (name, create_date, location, profile_picture)
        VALUES (?, ?, ?, ?)
    '''
    create_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    params = (name, create_date, location, profile_picture)
    execute_query(query, params)

@app.route('/accounts', methods=['POST'])
def create_account():
    data = request.form
    name, location, image_file = data.get('name'), data.get('location'), request.files.get('image')
    profile_picture = image_file.read() 
    try:
        insert_account(name, location, profile_picture)
        return jsonify({'success': 'Account created successfully'}), 201
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
