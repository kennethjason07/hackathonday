from flask import Flask, render_template, request
import psycopg2
import pandas as pd

app = Flask(__name__)

# Database configuration
DB_HOST = 'http://dpg-cpest0v79t8c73bdet8g-a.singapore-postgres.render.com/'
DB_NAME = 'bang_lore'
DB_USER = 'bang_lore_user'
DB_PASSWORD = 'GB9o29yszCItLrOGGBj5WgauI3E4ckfu'

# Function to connect to PostgreSQL database
def connect_to_db():
    return psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD)

# Route for the homepage
@app.route('/')
def index():
    return render_template('upload.html')

# Route to handle file upload and process data
@app.route('/upload', methods=['POST'])
def upload():
    if 'csvFile' not in request.files:
        return 'No file part'
    
    file = request.files['csvFile']
    if file.filename == '':
        return 'No selected file'

    if file:
        # Save the uploaded CSV file
        file.save('uploads/student_marks.csv')

        # Read the CSV file
        df = pd.read_csv('uploads/student_marks.csv')

        # Connect to PostgreSQL database
        conn = connect_to_db()
        cur = conn.cursor()

        # Insert data into PostgreSQL database
        for index, row in df.iterrows():
            student_name = row['Student_Name']
            parent_phone_number = row['Parent_Phone_Number']
            math_marks = row['Math']
            science_marks = row['Science']
            english_marks = row['English']
            history_marks = row['History']

            cur.execute("INSERT INTO student_marks (student_name, parent_phone_number, math_marks, science_marks, english_marks, history_marks) VALUES (%s, %s, %s, %s, %s, %s)",
                        (student_name, parent_phone_number, math_marks, science_marks, english_marks, history_marks))

        # Commit changes and close connection
        conn.commit()
        cur.close()
        conn.close()

        return 'File uploaded successfully and data inserted into database'

if __name__ == '__main__':
    app.run(debug=True)
