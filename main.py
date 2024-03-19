
from flask import Flask, render_template, request, redirect, url_for, Response, jsonify
from tqdm import tqdm
import hashlib
import sqlite3

app = Flask(__name__)


conn = sqlite3.connect('Project1.db')
cur = conn.cursor()
select_query = '''
SELECT email, password FROM User
'''
cur.execute(select_query)
rows = cur.fetchall()
email_password_dict = {}
with tqdm(total=len(rows), desc="Constructing dictionary") as pbar:
    for row in rows:
        email = row[0]
        password = row[1]
        email_password_dict[email] = password

        pbar.update(1)
        
cur.close()
conn.close()

@app.route('/')
def index():
    welcome_message = "Enter your email/password to verify"
    return render_template('check.html', welcome_message=welcome_message)

@app.route('/submit', methods=['POST'])
def submit():
    email_tmp = request.form['email_tmp']
    password_tmp = request.form['password_tmp']
    hashed_email = hashlib.sha256(email_tmp.strip().encode()).hexdigest()
    hashed_password = hashlib.sha256(password_tmp.strip().encode()).hexdigest()
    
    if(hashed_email in email_password_dict.keys()): 
        if (hashed_password == email_password_dict[hashed_email]):
            return "Your Current Email and Password have been compromised. Please change it!!" 
        else:
            return "This email is currently inside the database, however, the password is not the same."
    else:
        return "No entries found!!! Your account is safe!"

if __name__ == '__main__':
    app.run()
