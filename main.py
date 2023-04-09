from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'

# SQLite database connection
conn = sqlite3.connect('users.db')
c = conn.cursor()

# Create users table
c.execute('''CREATE TABLE IF NOT EXISTS users
             (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, email TEXT NOT NULL, password TEXT NOT NULL)''')
conn.commit()

# Register API
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    name = data['name']
    email = data['email']
    password = data['password']

    c.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
              (name, email, password))
    conn.commit()

    return jsonify({'message': 'User registered successfully!'})

# Login API
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data['email']
    password = data['password']

    c.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
    user = c.fetchone()

    if user:
        return jsonify({'message': 'Login successful!'})
    else:
        return jsonify({'message': 'Invalid email or password'}), 401

# Get all users API
@app.route('/users', methods=['GET'])
def get_users():
    c.execute("SELECT * FROM users")
    users = c.fetchall()

    user_list = []
    for user in users:
        user_dict = {'id': user[0], 'name': user[1], 'email': user[2], 'password': user[3]}
        user_list.append(user_dict)

    return jsonify({'users': user_list})

# Get user by ID API
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    c.execute("SELECT * FROM users WHERE id=?", (user_id,))
    user = c.fetchone()

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

    c.execute("UPDATE users SET name=?, email=?, password=? WHERE id=?",
              (name, email, password, user_id))
    conn.commit()

    return jsonify({'message': 'User updated successfully!'})

# Delete user API
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    c.execute("DELETE FROM users WHERE id=?", (user_id,))
    conn.commit()

    return jsonify({'message': 'User deleted successfully!'})

if __name__ == '__main__':
    app.run(debug=True)
