import sqlite3
from flask import flash
from datetime import datetime

def signup(username, password, favorite_color, password_hint, assigned_tasks):
    connection = sqlite3.connect('users.db', check_same_thread= False)
    cursor = connection.cursor()
    cursor.execute(""" SELECT password FROM users where username = '{username}';""".format(username = username))
    exist = cursor.fetchone()

    if exist is None:
        cursor.execute(""" INSERT INTO users(username, password, favorite_color, password_hint, assigned_tasks) VALUES('{username}','{password}', '{favorite_color}', '{password_hint}', '{assigned_tasks}');""".format(username = username, password = password, favorite_color = favorite_color, password_hint = password_hint, assigned_tasks = assigned_tasks))
        connection.commit()
        cursor.close()
        connection.close()
        exit()
    else:
        return ('User already exists!!!')
    
    return 'You have successfully signed up!!!'



def check_user(username):
    connection = sqlite3.connect('users.db', check_same_thread= False)
    cursor = connection.cursor()
    try:
        cursor.execute(""" SELECT username FROM users where username = '{username}';""".format(username = username))
        exist = cursor.fetchone()[0]
        return exist
    except:
        return "no such user"

def check_admin(username):
    connection = sqlite3.connect('users.db', check_same_thread= False)
    cursor = connection.cursor()
    try:
        cursor.execute(""" SELECT username FROM admin where username = '{username}';""".format(username = username))
        exist = cursor.fetchone()[0]
        return exist
    except:
        return "no such user"

def check_pw(username):
    connection = sqlite3.connect('users.db', check_same_thread=False)
    cursor = connection.cursor()
    cursor.execute(""" SELECT password FROM users WHERE username = '{username}' ORDER BY ID DESC;""".format(username = username))
    password = cursor.fetchone()[0]
    connection.commit()
    cursor.close()
    connection.close()
    return password
 

def admin_check_pw(username):
    connection = sqlite3.connect('users.db', check_same_thread=False)
    cursor = connection.cursor()
    cursor.execute("""SELECT password FROM admin where username = \'{username}\' ORDER BY id DESC;""".format(username=username))
    password = cursor.fetchone()[0]
    connection.commit()
    cursor.close()
    connection.close()
    return password

def all_users(connection = sqlite3.connect('users.db')):    
    cursor = connection.cursor()
    users = cursor.execute("""SELECT username FROM users;""")
    #users = cursor.fetchone()[0]
    connection.commit()
    cursor.close()
    connection.close()
    print(users)



def assign_tasks(username, assigned_tasks):
    connection = sqlite3.connect('users.db', check_same_thread=False)
    cursor = connection.cursor()    
    cursor.execute("""UPDATE users SET assigned_tasks = '{assigned_tasks}' WHERE username = '{username}';""".format(assigned_tasks=assigned_tasks, username = username))    
    connection.commit()
    cursor.close()
    connection.close()

def show_task(username):
    connection = sqlite3.connect('users.db', check_same_thread=False)
    cursor = connection.cursor()    
    cursor.execute("""SELECT assigned_tasks from users WHERE username = '{username}';""".format(username = username))
    value  = cursor.fetchone()[0]    
    connection.commit()
    cursor.close()
    connection.close()
    return value

def update_time(username):
    connection = sqlite3.connect('users.db', check_same_thread=False)
    cursor = connection.cursor()    
    cursor.execute("""UPDATE users SET last_login = '{date_time}' WHERE username = '{username}';""".format(date_time=datetime.now(), username = username))    
    connection.commit()
    cursor.close()
    connection.close()

def user_details(username):
    connection = sqlite3.connect('users.db', check_same_thread=False)
    cursor = connection.cursor()    
    cursor.execute("""SELECT * from users WHERE username = '{username}';""".format(username = username))
    value  = cursor.fetchone()
    connection.commit()
    cursor.close()
    connection.close()
    return value 

def user_stats():
    connection = sqlite3.connect('users.db', check_same_thread=False)
    cursor = connection.cursor()    
    new_signups = cursor.execute("""SELECT count(*) from users WHERE Timestamp >= date('now', '-1 days');""") 
    new_users  = new_signups.fetchone()[0]
    total = cursor.execute("""SELECT count(*) from users;""") 
    total_users = total.fetchone()[0]
    connection.commit()
    cursor.close()
    connection.close()
    return new_users, total_users 
