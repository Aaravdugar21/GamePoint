from flask import Flask, render_template, url_for, session, request, redirect
from users import create_account, check_account, create_table, create_table_for_games, add_new_game, delete_game_with_name
from database import get_db, get_game_db, close_db, close_game_db
from datetime import datetime

app = Flask(__name__)
app.secret_key = "3jf-*D[83SD83#8dfj@!"

app.teardown_appcontext(close_db)
app.teardown_appcontext(close_game_db)

with app.app_context():
    create_table()
    create_table_for_games()

def delete_expired_games():
    database = get_game_db()
    sql = database.cursor()
    current_datetime = datetime.now()
    current_date_str = current_datetime.strftime("%Y-%m-%d")
    current_time_str = current_datetime.strftime("%H:%M:%S")
    sql.execute('''DELETE FROM games WHERE date <= ? AND time <= ?''', [current_date_str, current_time_str])
    database.commit()

@app.route("/")
def index():
    # Print the session data for debugging
    print("Session:", session)  # Debugging line
    if session.get('logged_in'):
        return render_template("index.html")
    else:
        return render_template("index.html")  # Show the homepage even if not logged in

@app.route("/login", methods=['GET', 'POST'])
def login():
    error = ""
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        login_successful = check_account(username, password)
        if login_successful:
            session['logged_in'] = True  # Set the session variable
            return redirect(url_for('index'))  # Redirect to home after successful login
        else:
            error = "Wrong Username or Password"
    return render_template('login.html', error=error)

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == "GET":
        return redirect(url_for('login'))
    else:
        username = request.form['username']
        password = request.form['password']
        confirm = request.form['confirm-password']
        if password != confirm:
            msg = "Passwords don't match!"
        else:
            msg = create_account(username, password)
        return render_template("login.html", error=msg)

@app.route("/logout")
def logout():
    session.clear()  # Clear all session data
    return redirect(url_for('index'))  # Redirect to homepage

@app.route("/find_game")
def find_game():
    if session.get('logged_in'):
        delete_expired_games()
        database = get_game_db()
        sql = database.cursor()
        result = sql.execute('''SELECT * FROM games''')
        columns = [column[0] for column in result.description]
        games = [dict(zip(columns, row)) for row in result.fetchall()]

        for game in games:
            time_str = game['time']
            time_obj = datetime.strptime(time_str, "%H:%M")
            game['time'] = time_obj.strftime("%I:%M %p")

        return render_template("find_game.html", games=games)
    else:
        return redirect(url_for('login'))

@app.route("/create_game")
def create_game():
    if session.get('logged_in'):
        return render_template("create_game.html")
    else:
        return redirect(url_for('login'))

@app.route("/create_game_action", methods=['POST', 'GET'])
def create_game_action():
    sport = request.form['sport']
    requirement = request.form['requirement']
    name = request.form['name']
    address = request.form['address']
    state = request.form['state']
    city = request.form['city']
    zip = request.form['zip']
    date = request.form['date']
    time = request.form['time']
    description = request.form['description']
    phone = request.form['phone']
    email = request.form['email']
    level = request.form['level']
    add_new_game(sport, requirement, name, phone, email, level, address, state, city, zip, date, time, description)
    return redirect(url_for('find_game'))

@app.route("/about")
def about():
    return render_template("about.html")  # Always accessible, may require login for certain features

@app.route("/terms-of-use")
def terms_of_use():
    return render_template("termsofuse.html")  # Always accessible, may require login for certain features

@app.route("/privacy-policy")
def privacy_policy():
    return render_template("privacypolicy.html")  # Always accessible, may require login for certain features

if __name__ == "__main__":
    app.run(debug=True)
