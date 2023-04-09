from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'

# Register API
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    name = data['name']
    email = data['email']
    password = data['password']

    # Create a new database connection and cursor for this request
    conn = sqlite3.connect('users.db')
    c = conn.cursor()

    c.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
              (name, email, password))
    conn.commit()
    conn.close()

    return jsonify(name,email,password)

# Login API
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data['email']
    password = data['password']

    # Create a new database connection and cursor for this request
    conn = sqlite3.connect('users.db')
    c = conn.cursor()

    c.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
    user = c.fetchone()

    conn.close()

    if user:
        return jsonify({'message': 'Login successful!'})
    else:
        return jsonify({'message': 'Invalid email or password'}), 401

# Get all users API
@app.route('/users', methods=['GET'])
def get_users():
    # Create a new database connection and cursor for this request
    conn = sqlite3.connect('users.db')
    c = conn.cursor()

    c.execute("SELECT * FROM users")
    users = c.fetchall()

    user_list = []
    for user in users:
        user_dict = {'id': user[0], 'name': user[1], 'email': user[2], 'password': user[3]}
        user_list.append(user_dict)

    conn.close()

    return jsonify({'users': user_list})

# Get user by ID API
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    # Create a new database connection and cursor for this request
    conn = sqlite3.connect('users.db')
    c = conn.cursor()

    c.execute("SELECT * FROM users WHERE id=?", (user_id,))
    user = c.fetchone()

    conn.close()

    if user:
        user_dict = {'id': user[0], 'name': user[1], 'email': user[2], 'password': user[3]}
        return jsonify({'user': user_dict})
    else:
        return jsonify({'message': 'User not found'}), 404

# Update user API
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    name = data['name']
    email = data['email']
    password = data['password']

    # Create a new database connection and cursor for this request
    conn = sqlite3.connect('users.db')
    c = conn.cursor()

    c.execute("UPDATE users SET name=?, email=?, password=? WHERE id=?",
              (name, email, password, user_id))
    conn.commit()
    conn    
    c.close()
    conn.close()

    return jsonify({'message': 'User updated successfully!'})

# Delete user API
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    # Create a new database connection and cursor for this request
    conn = sqlite3.connect('users.db')
    c = conn.cursor()

    c.execute("DELETE FROM users WHERE id=?", (user_id,))
    conn.commit()
    conn.close()

    return jsonify({'message': 'User deleted successfully!'})


if __name__ == '__main__':
    # Create the users table if not exists
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 name TEXT, email TEXT, password TEXT)''')
    conn.commit()
    conn.close()

    app.run(debug=True)


