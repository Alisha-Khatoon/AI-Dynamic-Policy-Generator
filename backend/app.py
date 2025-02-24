
import os
import google.generativeai as genai
import psycopg2
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

# PostgreSQL Connection
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")

conn = psycopg2.connect(
    dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT
)
cursor = conn.cursor()

# Create table if not exists
cursor.execute("""
    CREATE TABLE IF NOT EXISTS policies (
        id SERIAL PRIMARY KEY,
        industry VARCHAR(255) NOT NULL,
        compliance VARCHAR(255) NOT NULL,
        policy TEXT NOT NULL,
        UNIQUE(industry, compliance)
    );
""")
conn.commit()

# Initialize Flask app
app = Flask(__name__)
CORS(app)

@app.route('/generate-policy', methods=['POST'])
def generate_policy():
    try:
        data = request.json
        industry = data.get("industry", "General")
        compliance = data.get("compliance", "GDPR")

        # Check if policy already exists
        cursor.execute(
            "SELECT policy FROM policies WHERE industry = %s AND compliance = %s",
            (industry, compliance),
        )
        existing_policy = cursor.fetchone()

        if existing_policy:
            return jsonify({
                "message": "Policy retrieved from database",
                "policy": existing_policy[0]
            })

        # Generate new policy
        prompt = f"""
        Generate a structured company policy for {industry} that complies with {compliance} regulations.
        The policy should include:
        1️⃣ Purpose
        2️⃣ Scope
        3️⃣ Definitions
        4️⃣ Compliance Principles
        5️⃣ Responsibilities
        6️⃣ Specific Requirements
        7️⃣ Compliance Monitoring
        8️⃣ Consequences of Non-Compliance
        """
        model = genai.GenerativeModel("gemini-pro")  
        response = model.generate_content(prompt)

        if not response.text:
            return jsonify({"error": "Failed to generate policy"}), 500

        # Save to PostgreSQL
        cursor.execute(
            "INSERT INTO policies (industry, compliance, policy) VALUES (%s, %s, %s) ON CONFLICT (industry, compliance) DO NOTHING",
            (industry, compliance, response.text.strip()),
        )
        conn.commit()

        return jsonify({
            "message": "Policy generated and saved",
            "policy": response.text.strip()
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/get-policy', methods=['GET'])
def get_policy():
    try:
        industry = request.args.get("industry", "General")
        compliance = request.args.get("compliance", "GDPR")

        cursor.execute(
            "SELECT policy FROM policies WHERE industry = %s AND compliance = %s",
            (industry, compliance),
        )
        policy = cursor.fetchone()

        if policy:
            return jsonify({"policy": policy[0]})
        else:
            return jsonify({"error": "Policy not found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/update-policy', methods=['PUT'])
def update_policy():
    try:
        data = request.json
        industry = data.get("industry")
        compliance = data.get("compliance")
        new_policy = data.get("policy")

        if not industry or not compliance or not new_policy:
            return jsonify({"error": "Missing required fields"}), 400

        cursor.execute(
            "UPDATE policies SET policy = %s WHERE industry = %s AND compliance = %s RETURNING policy",
            (new_policy, industry, compliance),
        )
        updated_policy = cursor.fetchone()

        if updated_policy:
            conn.commit()
            return jsonify({"message": "Policy updated successfully", "policy": updated_policy[0]})
        else:
            return jsonify({"error": "Policy not found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
