from flask import Flask, jsonify
import mysql.connector
import random
import os

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv('DB_HOST', 'mysql'),
        user=os.getenv('DB_USER', 'appuser'),
        password=os.getenv('DB_PASSWORD', 'apppassword123'),
        database=os.getenv('DB_NAME', 'appdb')
    )

@app.route('/api/health')
def health():
    return jsonify({"status": "healthy"})

@app.route('/api/users')
def get_users():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(users)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/init-db')
def init_db():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100),
                email VARCHAR(100)
            )
        """)
        cursor.execute("""
            INSERT INTO users (name, email) VALUES
            ('John Doe', 'john@example.com'),
            ('Jane Smith', 'jane@example.com')
        """)
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Database initialized"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
funny_first_names = [
    "Giga", "Ultra", "Mega", "Baby", "Sneaky", "Chonky", "Sir", "Professor", "Doctor", "Mister"
]

funny_last_names = [
    "Noodle", "Thunder", "McFluff", "Wobbles", "Bananapants", "Destroyer", "Pickleface", "Boomer", "Gooner"
]

@app.route('/api/random-user')
def random_user():
    name = f"{random.choice(funny_first_names)} {random.choice(funny_last_names)}"
    email = name.lower().replace(" ", ".") + "@hotmail.com"
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
                INSERT INTO users (name, email) VALUES
                ('""" + name + """', '""" + email + """')""")
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Random user added"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route("/api/wisdom")
def wisdom():
    wisdoms = [
        "Man who drop watch in toilet has shitty time",
        "Man who runs in front of car gets tired. Man who runs behind car gets exhausted",
        "Man who wants to date pretty nurse must be patient.",
        "Man with hand in pants feel cocky all day .",
        "Man who run behind car will get exhausted but man who runs in front of car will get tyred.",
        "Man who walk into airport doors sideways, going to Bangkok.",
        "水果喂没有那时候",
        "菜住现在想她",
        "千里之行，始于足下",
        "学而不思则罔，思而不学则殆",
        "知之为知之，不知为不知，是知也",
    ]
    choice = random.choice(wisdoms)
    return jsonify({"wisdom": choice})



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5022)