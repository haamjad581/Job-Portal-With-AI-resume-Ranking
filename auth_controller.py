# ===================
# Routes
# ===================

@auth_ns.route("/register")
class Register(Resource):
    @auth_ns.expect(register_model, validate=True)
    @auth_ns.response(201, "Created", message_model)
    @auth_ns.response(400, "Bad Request", error_model)
    def post(self):
        """Register a new user"""
        data = request.json
        name = data['name']
        email = data['email']
        password = hashlib.sha256(data['password'].encode()).hexdigest()

        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)", 
                           (name, email, password))
            conn.commit()
            return {"message": "User registered successfully"}, 201
        except mysql.connector.IntegrityError:
            return {"error": "Email already exists"}, 400
        finally:
            cursor.close()
            conn.close()


@auth_ns.route("/login")
class Login(Resource):
    @auth_ns.expect(login_model, validate=True)
    @auth_ns.response(200, "OK", message_model)
    @auth_ns.response(401, "Unauthorized", error_model)
    def post(self):
        """Login with email and password"""
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
            return {"message": "Login successful", "user": user}, 200
        else:
            return {"error": "Invalid email or password"}, 401


@auth_ns.route("/me")
class Me(Resource):
    @auth_ns.response(200, "OK")
    @auth_ns.response(401, "Unauthorized", error_model)
    def get(self):
        """Get current logged-in user"""
        if 'user_id' in session:
            return {"user_id": session['user_id']}, 200
        else:
            return {"error": "Not logged in"}, 401


# ===================
# Run App
# ===================
if __name__ == '__main__':
    app.run(debug=True)