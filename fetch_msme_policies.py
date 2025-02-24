import requests
import psycopg2
from datetime import datetime

# PostgreSQL Connection
DB_CONFIG = {
    "dbname": "policy_db",
    "user": "postgres",
    "password": "21lish@",
    "host": "localhost",
    "port": "5432"
}

# ✅ Fixed API URL
API_URL = "https://api.data.gov.in/resource/47d1657d-4183-46ed-bfc2-0b9a5694a742?api-key=579b464db66ec23bdd000001678f6cc1e45a420b6e155987d71d6049&format=json"

# Function to Fetch MSME Policies
def fetch_policies():
    try:
        response = requests.get(API_URL)
        if response.status_code == 200:
            data = response.json()
            return data.get("records", [])  # ✅ Ensures a list is returned
        else:
            print(f"Error fetching data: {response.status_code}")
            return []
    except Exception as e:
        print(f"API Request Error: {e}")
        return []

# Function to Insert Data into PostgreSQL
def insert_into_db(policies):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()

        for policy in policies:
            created_date_str = policy.get("createddate")
            if created_date_str:
                try:
                    created_date = datetime.strptime(created_date_str, "%Y-%m-%dT%H:%M:%S.%f")
                except ValueError:
                    created_date = None  # Handle incorrect/missing date format
            else:
                created_date = None

            cursor.execute("""
                INSERT INTO msme_policies (state_name, district_name, total_no_of_applications, total_no_of_micro, total_no_of_small, total_no_of_medium, created_date)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                policy.get("statename", ""),
                policy.get("districtname", ""),
                policy.get("totalnoofapplication", 0),
                policy.get("totalnoof_micro", 0),
                policy.get("totalnoof_small", 0),
                policy.get("totalnoof_medium", 0),
                created_date
            ))

        conn.commit()
        print("✅ Data inserted successfully!")

    except Exception as e:
        print("❌ Database Error:", e)

    finally:
        cursor.close()
        conn.close()

# Main Execution
if __name__ == "__main__":
    policies = fetch_policies()
    if policies:
        insert_into_db(policies)  # ✅ Fixed
