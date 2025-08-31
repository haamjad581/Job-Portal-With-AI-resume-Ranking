print(">>> app.py is starting...")

from flask import Flask
from flask_restx import Api

# Import our auth controller
from auth_controller import auth_ns

app = Flask(__name__)

api = Api(
    app,
    version="1.0",
    title="JobPortal Auth API",
    description="Simple auth endpoints with static validation",
    doc="/docs"  # Swagger UI
)

# Register namespaces
api.add_namespace(auth_ns, path="/auth")


@app.route("/")
def home():
    return "Hello Flask is my first project!"


if __name__ == "__main__":
    print(">>> flask")
    app.run(debug=True)
