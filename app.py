from flask import Flask, jsonify
import os
import psycopg2
import docker

app = Flask(__name__)

def read_password_from_file(file_path):
    with open(file_path, 'r') as file:
        db_password = file.read().strip()
    return db_password

CONTAINER_NAME = os.environ.get("CONTAINER_NAME")
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_USER = os.environ.get("DB_USER")
DB_NAME = os.environ.get("DB_NAME")
DB_PASSWORD_FILE = os.environ.get("DB_PASSWORD_FILE")

# Get the password from the docker secret
db_password = read_password_from_file(DB_PASSWORD_FILE)

def db_connect():
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=db_password,
        database=DB_NAME
    )
    return conn

def check_db_connection():
    try:
        conn = db_connect()
        conn.close()
        return True
    except psycopg2.OperationalError:
        return False


def get_table_count():
    conn = db_connect()
    cur = conn.cursor()
    cur.execute("SELECT count(*) FROM information_schema.tables")
    count = cur.fetchone()[0]
    cur.close()
    conn.close()
    return count

@app.route('/health')
def health():
    if check_db_connection():
        return jsonify({"status": "Healthy!", "container": CONTAINER_NAME}), 200
    else:
        return jsonify({"status": "Unhealthy", "container": CONTAINER_NAME}), 503

@app.route('/number_of_tables')
def number_of_tables():
    table_count = get_table_count()
    return jsonify({"number_of_tables": str(table_count)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
