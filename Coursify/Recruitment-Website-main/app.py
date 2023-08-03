from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# MySQL database configuration
db = mysql.connector.connect(
    host="your_host",
    user="your_username",
    password="your_password",
    database="your_database"
)

# Function to create the database table
def create_table():
    cursor = db.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS job_openings (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            description TEXT,
            location VARCHAR(100),
            job_type VARCHAR(50)
        )
    """)
    db.commit()

# Home page - displays the list of job openings
@app.route('/')
def index():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM job_openings")
    job_openings = cursor.fetchall()
    return render_template('index.html', job_openings=job_openings)

# Add a new job opening to the database
@app.route('/add', methods=['POST'])
def add_job_opening():
    title = request.form['title']
    description = request.form['description']
    location = request.form['location']
    job_type = request.form['job_type']

    cursor = db.cursor()
    cursor.execute("""
        INSERT INTO job_openings (title, description, location, job_type)
        VALUES (%s, %s, %s, %s)
    """, (title, description, location, job_type))
    db.commit()

    return redirect(url_for('index'))

if __name__ == '__main__':
    create_table()
    app.run(debug=True)
