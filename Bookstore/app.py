from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3

app = Flask(__name__)
app.secret_key = "your_secret_key" 

@app.route('/')
def index():
    return render_template('index.html')

# database
def init_db():
    conn = sqlite3.connect('Models/database.db')
    cursor = conn.cursor()
    
    #users table
    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        )
    ''')
    
    # products table
    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS products(
            product_id INTEGER PRIMARY KEY,
            product_category INTEGER,
            product_name TEXT,
            product_description TEXT,
            product_price FLOAT,
            product_quantity INTEGER
        )
    ''')

    # Customers profiles
    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS customers_profiles (
            user_id INTEGER PRIMARY KEY,
            first_name TEXT,
            last_name TEXT,
            birth_date TEXT,
            age INTEGER,
            gender TEXT,
            phone TEXT,
            country TEXT,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    ''')
    
    
    conn.commit()
    
    # new default users
    cursor.execute("INSERT OR IGNORE INTO users (username, password, role) VALUES (?, ?, ?)", 
                   ('admin', 'admin123', 'admin'))
    cursor.execute("INSERT OR IGNORE INTO users (username, password, role) VALUES (?, ?, ?)", 
                   ('customer', 'customer123', 'customer'))
    conn.commit()
    conn.close()

#categories
@app.route ('/categories')
def categories():
    return render_template('categories.html')

#sci-fi category
@app.route ('/scifi')
def scifi():
    return render_template('scifi.html')

#fantasy category
@app.route('/fantasy')
def fantasy():
    return render_template('fantasy.html')

#horror category
@app.route('/horror')
def horror():
    return render_template('horror.html')

#comics category
@app.route('/comics')
def comics():
    return render_template('comics.html')

#contact
@app.route ('/contact')
def contact():
    return render_template('contact.html')

# login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect('Models/database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            session['username'] = user[1]
            session['role'] = user[3]
            session['user_id'] = user[0] 
            if user[3] == 'admin':
                return redirect(url_for('admin_side'))
            elif user[3] == 'customer':
                return redirect(url_for('client_side'))
        else:
            flash("Username or password incorrect.")
    return render_template('login.html')

#register
@app.route ('/register')
def register():
    return render_template('register.html')

if __name__ == '__main__':
    init_db() 
    app.run(debug=True)