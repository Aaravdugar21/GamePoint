from database import get_db, get_game_db
import bcrypt

def create_table():
    database = get_db()
    sql = database.cursor()
    sql.execute('''create table if not exists users(
                userId integer primary key autoincrement,
                username text,
                password text
    )''')

def create_account(username, password):
    database = get_db()
    sql = database.cursor()
    result = sql.execute('''select * from users where username = ?''', [username])
    rows = result.fetchall()
    row_count = len(rows)
    if row_count > 0:
        return "Can't create account. Username already exists."
    else:
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        sql.execute('''INSERT into users (username, password) values (?, ?)''', [username, hashed_password])
        database.commit()
        return "Successfully Created Account"
    
def check_account(username, password):
    database = get_db()
    sql = database.cursor()
    result = sql.execute('''select * from users where username = ?''', [username])
    row = result.fetchone()
    if row:
        hashed_password = row[2]
        if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
            return True
    return False

def create_table_for_games():
    database = get_game_db()
    sql = database.cursor()
    sql.execute('''CREATE TABLE IF NOT EXISTS games(
                gameId integer primary key autoincrement,
                sport text not null,
                requirement text not null,
                name text not null,
                phone text not null,
                email text not null,
                level text not null,
                address text not null,
                city text not null,
                state text not null,
                zip text not null,
                date text not null,
                time text not null,
                description text not null,
                joined integer default 0
    )''')

def add_new_game(sport, requirement, name, phone, email, level, address, city, state, zip, date, time, description):
    database = get_game_db()
    sql = database.cursor()
    sql.execute('''INSERT INTO games (sport, requirement, name, phone, email, level, address, city, state, zip, date, time, description) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) ''', [sport, requirement, name, phone, email, level, address, city, state, zip, date, time, description])
    database.commit()
    return "Successfully Created Game"

def delete_game_with_name(input_name):
    database = get_game_db()
    sql = database.cursor()
    sql.execute('''DELETE FROM games WHERE name=?''',[input_name])
