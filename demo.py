from flask import Flask, render_template, flash, request, session, redirect, url_for, g
from datetime import datetime
import model 
import sqlite3


app = Flask(__name__)

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


@app.route('/', methods = ['GET', 'POST'])
def home():
    if request.method == 'GET':
        return render_template("home.html")
    if request.method == 'POST':
        session.pop('username', None)
        username = request.form['username']
        password = request.form['password']
        user = model.check_user(username)
        try:
            pwd = model.check_pw(username)
            if username == user and pwd == password:
                session['username'] = request.form['username']
                session['logged_in'] = True
                title = session['username']
                model.update_time(username)
                return redirect(url_for('dashboard'))
        except:
            error = "Username Error"
            return render_template('home.html', error = error)
        error = "Authentication Error"
        return render_template('home.html', error = error)
    return redirect(url_for('dashboard'))

    

@app.route('/admin', methods = ['GET', 'POST'])
def admin():
    if request.method == 'GET':
        return render_template("admin.html")
    if request.method == 'POST':
        session.pop('username', None)
        username = request.form['username']
        password = request.form['password']
        user = model.check_admin(username)
        try:
            pwd = model.admin_check_pw(username)
            if username == user and pwd == password:
                session['username'] = request.form['username']
                session['logged_in'] = True
                session_user = session['username']
                conn = sqlite3.connect('users.db')
                cursor = conn.execute("SELECT * from users order by last_login desc")
                names = conn.execute("SELECT * from users")
                new_users = model.user_stats()
                totalusers = model.user_stats()
                assign = model.assign_tasks
                dates = datetime.now().strftime('%Y-%m-%d %H:%M:%S')   
                return render_template('admin_dashboard.html', users = cursor, assign= assign, names = names, dates = dates, new_users = new_users, totalusers = totalusers, title="Admin Page", session_user = session_user)
                conn(close)
        except:
            error = "Username Error"
            return render_template('admin.html', error = error)
        error = "Authentication Error"
        return render_template('admin.html', error = error)
    return redirect(url_for('admin'))

        
@app.route('/about', methods = ['GET'])
def about():
    return render_template('about.html', title="About")

@app.route('/dashboard', methods = ['GET'])
def dashboard():
    if 'username' in session:
        task = model.show_task(session['username'])        
        return render_template('dashboard.html', title="Dashboard", task = task)
    return redirect(url_for('home'))

@app.route('/admin_dashboard', methods = ['GET'])
def admin_dashboard():
    if 'username' in session:
        session_user = session['username']
        conn = sqlite3.connect('users.db')
        cursor = conn.execute("SELECT * from users order by Timestamp desc")
        names = conn.execute("SELECT * from users")             
        new_users = model.user_stats()
        totalusers = model.user_stats()
        assign = model.assign_tasks
        dates = datetime.now().strftime('%Y-%m-%d %H:%M:%S')   
        return render_template('admin_dashboard.html', users = cursor, assign= assign, names = names, dates = dates, new_users = new_users, totalusers = totalusers, title="Admin Page", session_user = session_user)
        conn(close)
    return redirect(url_for('admin'))


@app.route('/user/<username>', methods=['GET'])
def user(username):
    try:
        if session['username']=='admin':
            users = model.user_details(username)
            #return render_template('user.html')
            title = "users"
            return render_template('user.html', users = users, title = title)
    except:
        return render_template('admin.html')
        
    

@app.route('/policy', methods = ['GET'])
def policy():
    return render_template('policy.html', title="Policy")

@app.route('/signup', methods = ['GET', 'POST'])
def signup():
    if request.method == 'GET':
        message = 'Please sign up!'
        return render_template('signup.html', message = message, header = message, title="Sign up here!")
    else:
        username = request.form['username']
        password = request.form['password']
        favorite_color = request.form["favorite_color"]
        password_hint = request.form["password_hint"]
        assigned_tasks = request.form["assigned_tasks"]
        message = model.signup(username, password, favorite_color, password_hint, assigned_tasks)
        return render_template('home.html', message = message, header = message, title="Home")

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        session.pop('username', None)
        username = request.form['username']
        password = request.form['password']
        pwd = model.check_user(username)
        if pwd is not None:
            session['username'] = request.form['username']
            session['logged_in'] = True
            message = "success"
            return redirect(url_for('home', message = message))
        return "invalid user"
    else:
        error = 'Invalid login'
        return render_template('login.html', error = error, title=error)      
        return render_template('login.html', title="Login")




@app.route('/assign', methods=['GET','POST'])
def assign():
    if request.method == 'POST':
        assigned_tasks = request.form["assigned_tasks"]
        username = request.form["username"]   
        insert = model.assign_tasks(username, assigned_tasks)
        conn = sqlite3.connect('users.db')
        cursor = conn.execute("SELECT * from users order by Timestamp desc")        
        message = "Post success"
        return render_template('admin_dashboard.html', message = message, users = cursor , title='Assign Tasks')
        conn(close)

@app.route('/logout', methods=['GET'])
def logout():
    session.clear()
    flash('Your are now logged out', 'success')
    return redirect(url_for('home'))

@app.route('/admin_logout', methods=['GET'])
def admin_logout():
    session.clear()
    flash('Your are now logged out', 'success')
    return redirect(url_for('admin'))




if __name__ == '__main__':
    app.secret_key='secret123'
    app.run(port = 7000, debug=True) 