import os
import json
from datetime import datetime

import mysql.connector
from flask import Flask, render_template

app = Flask(__name__)

def get_db_uptime():
    conn = mysql.connector.connect(
        host=os.environ['db_host'],
        user=os.environ['db_user'],
        password=os.environ['db_pass'],
        database=os.environ['db_name']
    )
    cursor = conn.cursor()
    cursor.execute("SELECT NOW()")
    result = cursor.fetchone()
    result = result[0].strftime("%Y-%m-%d %H:%M:%S")

    # Clean up
    cursor.close()
    conn.close()

    return(result)

@app.route('/')
def gooning():
    time = get_db_uptime()
    return render_template('PirateWeb.html', sql_server_time=time)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)