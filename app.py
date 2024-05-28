from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from mysql.connector import errorcode
from werkzeug.security import generate_password_hash
import os
from dotenv import load_dotenv

load_dotenv('configPass.env')
app = Flask(__name__)

# Function to get a database connection
def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host=os.getenv('MYSQL_HOST', 'localhost'),
            user=os.getenv('MYSQL_USER', 'dself1976'),
            password=os.getenv('MYSQL_PASSWORD', 'Max123max123'),
            database=os.getenv('MYSQL_DB', 'newsociopedia'),
            auth_plugin='caching_sha2_password'
        )
        return conn
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Error: Something is wrong with your username or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Error: Database does not exist")
        else:
            print(f"Error: {err}")
        return None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        hashed_password = generate_password_hash(request.form['password'])
        sex = request.form['sex']
        country = request.form['country']
        state = request.form['state']

        conn = get_db_connection()
        if conn is not None:
            cursor = conn.cursor()
            try:
                cursor.execute('''
                    INSERT INTO users (first_name, last_name, email, password, sex, country, state) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                ''', (first_name, last_name, email, hashed_password, sex, country, state))
                conn.commit()
            except mysql.connector.Error as err:
                print(f"Failed inserting data into MySQL table: {err}")
                conn.rollback()
            finally:
                cursor.close()
                conn.close()

        return redirect(url_for('home'))

    return render_template('regForm.html')

def create_users_table():
    conn = get_db_connection()
    if conn is not None:
        cursor = conn.cursor()
        try:
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    first_name VARCHAR(50),
                    last_name VARCHAR(50),
                    email VARCHAR(100) UNIQUE,
                    password VARCHAR(255) NOT NULL,
                    sex ENUM('male', 'female', 'other'),
                    country VARCHAR(50),
                    state VARCHAR(50),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()
        except mysql.connector.Error as err:
            print(f"Failed creating database table: {err}")
        finally:
            cursor.close()
            conn.close()

if __name__ == '__main__':
    create_users_table()
    app.run(debug=True)
