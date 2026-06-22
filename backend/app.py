from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
import os

app = Flask(__name__)
#CORS(app)
CORS(app, resources={r"/*": {"origins": "*"}})


# Database Configuration
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", "aryanverma"),
    "database": os.getenv("DB_NAME", "employee_db")

}


def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)


@app.route("/")
def home():
    return jsonify({
        "message": "Employee Management API is running"
    })


@app.route("/employees", methods=["GET"])
def get_employees():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM employees")
        employees = cursor.fetchall()

        cursor.close()
        conn.close()

        return jsonify(employees)

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


@app.route("/employee", methods=["POST"])
def add_employee():
    try:
        data = request.get_json()

        name = data.get("name")

        if not name:
            return jsonify({
                "error": "Employee name is required"
            }), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        query = "INSERT INTO employees (name) VALUES (%s)"
        cursor.execute(query, (name,))

        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({
            "message": "Employee added successfully"
        }), 201

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5050,
        debug=True
    )