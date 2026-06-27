import os
import sys
import mysql.connector
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

def run():
    print("Connecting to Aiven database...")
    try:
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST", "localhost"),
            port=int(os.getenv("DB_PORT", 3306)),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD", ""),
            database=os.getenv("DB_NAME", "cartlytics"),
            charset="utf8mb4",
            autocommit=True,
            auth_plugin="mysql_native_password"
        )
        print("Connected successfully!")
    except Exception as e:
        print(f"Connection failed: {e}")
        sys.exit(1)

    schema_path = os.path.join(os.path.dirname(__file__), "..", "database", "migrations", "001_initial_schema.sql")
    
    with open(schema_path, 'r', encoding='utf-8') as f:
        sql = f.read()

    print("Executing schema migrations...")
    cur = conn.cursor()
    
    # Execute the SQL script (multi=True handles multiple statements separated by ;)
    try:
        results = cur.execute(sql, multi=True)
        for result in results:
            pass # Consume the results to ensure execution completes
        print("Schema successfully created!")
    except Exception as e:
        print(f"Error executing schema: {e}")
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    run()
