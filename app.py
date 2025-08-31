from flask import Flask, request, jsonify, session
import mysql.connector
import hashlib
from flasgger import Swagger, swag_from

app = Flask(__name__)
app.secret_key = "secret123"   # session ke liye

# 🔹 Swagger Config
app.config['SWAGGER'] = {
    'title': 'Job Portal API',
    'uiversion': 3
}
swagger = Swagger(app)

# Database connection
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",   # apna password yahan dalna
        database="jobportal"
    )

# 🔹 Register user
@app.route('/register', methods=['POST'])
@swag_from({
    'tags': ['Auth'],
    'description': 'Register a new user',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'properties': {
                    'name': {'type': 'string'},
                    'email': {'type': 'string'},
                    'password': {'type': 'string'}
                },
                'required': ['name', 'email', 'password']
            }
        }
    ],
    'responses': {
        200: {'description': 'User registered successfully'},
        400: {'description': 'Email already exists'}
    }
})
def register():
    data = request.json
    name = data['name']
    email = data['email']
    password = hashlib.sha256(data['password'].encode()).hexdigest()  # password hash

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)", 
                       (name, email, password))
        conn.commit()
        return jsonify({"message": "User registered successfully"})
    except mysql.connector.IntegrityError:
        return jsonify({"error": "Email already exists"}), 400
    finally:
        cursor.close()
        conn.close()

# 🔹 Login user
@app.route('/login', methods=['POST'])
@swag_from({
    'tags': ['Auth'],
    'description': 'Login user',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'properties': {
                    'email': {'type': 'string'},
                    'password': {'type': 'string'}
                },
                'required': ['email', 'password']
            }
        }
    ],
    'responses': {
        200: {'description': 'Login successful'},
        401: {'description': 'Invalid email or password'}
    }
})
def login():
    data = request.json
    email = data['email']
    password = hashlib.sha256(data['password'].encode()).hexdigest()

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE email=%s AND password=%s", (email, password))
    user = cursor.fetchone()
    cursor.close()
    conn.close()

    if user:
        session['user_id'] = user['id']
        return jsonify({"message": "Login successful", "user": user})
    else:
        return jsonify({"error": "Invalid email or password"}), 401

# 🔹 Current user (test login session)
@app.route('/me', methods=['GET'])
@swag_from({
    'tags': ['User'],
    'description': 'Get current logged-in user',
    'responses': {
        200: {'description': 'Returns user ID from session'},
        401: {'description': 'Not logged in'}
    }
})
def me():
    if 'user_id' in session:
        return jsonify({"user_id": session['user_id']})
    else:
        return jsonify({"error": "Not logged in"}), 401

if __name__ == '__main__':
    app.run(debug=True)
