from flask import Flask, jsonify
import psycopg2

app = Flask(__name__)

# Database Configuration
DB_CONFIG = {
    "dbname": "policy_db",
    "user": "postgres",
    "password": "21lish@",
    "host": "localhost",
    "port": "5432"
}

# API Route to Fetch All Policies
@app.route('/policies', methods=['GET'])
def get_policies():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM msme_policies;")
        policies = cursor.fetchall()
        cursor.close()
        conn.close()

        # Convert data to JSON format
        policies_list = [
            {
                "id": row[0],
                "state_name": row[1],
                "district_name": row[2],
                "total_no_of_applications": row[3],
                "total_no_of_micro": row[4],
                "total_no_of_small": row[5],
                "total_no_of_medium": row[6],
                "created_date": row[7].strftime("%Y-%m-%d %H:%M:%S")
            }
            for row in policies
        ]

        return jsonify(policies_list)

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
